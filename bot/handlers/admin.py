import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest, TelegramNotFound

from bot.config import PAPA_ID
from bot.catalog_data import BASE_PRODUCTS
from bot.keyboards.admin import (
    get_admin_menu,
    get_admin_categories_keyboard,
    get_admin_products_keyboard,
    get_admin_edit_fields_keyboard,
    get_admin_edit_categories_keyboard,
    get_admin_edit_image_keyboard,
    get_admin_skip_image_keyboard,
    get_admin_cancel_keyboard,
)
from bot.locales import CATEGORY_NAMES, LANGUAGES
from bot.services.catalog import (
    get_all_products,
    get_product,
    add_product,
    delete_product,
    update_product,
    format_price,
)
from bot.states import AdminState
from bot.utils import get_lang

logger = logging.getLogger(__name__)

# Черновик нового товара во время добавления
new_product: dict = {}

ADMIN_MENU_TEXT = (
    "🛠 <b>Admin panel</b>\n\n"
    "Bu yerda siz mahsulotlarni boshqarishingiz mumkin.\n"
    "Здесь вы можете управлять товарами."
)


def _reset_draft() -> None:
    new_product.clear()


def _is_admin(obj) -> bool:
    user = getattr(obj, "from_user", None)
    if not user:
        return False
    return bool(PAPA_ID) and user.id == PAPA_ID


def _escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


async def _edit_or_answer(call: types.CallbackQuery, text: str, markup) -> None:
    """Пробует отредактировать сообщение, иначе шлёт новое."""
    try:
        await call.message.edit_text(text, reply_markup=markup)
    except (TelegramBadRequest, TelegramNotFound):
        await call.message.answer(text, reply_markup=markup)


def register_handlers(dp: Dispatcher, bot: Bot) -> None:
    # --- Вход в админку ---

    @dp.message(Command("admin"))
    async def admin_entry(message: types.Message, state: FSMContext):
        if not _is_admin(message):
            await message.answer(
                "⛔️ Bu bo'lim faqat admin uchun! / Этот раздел только для админа!"
            )
            return

        await state.set_state(AdminState.menu)
        await message.answer(ADMIN_MENU_TEXT, reply_markup=get_admin_menu())

    # --- Навигация ---

    @dp.callback_query(F.data == "admin_menu")
    async def admin_menu_back(call: types.CallbackQuery, state: FSMContext):
        _reset_draft()
        await state.set_state(AdminState.menu)
        await _edit_or_answer(call, ADMIN_MENU_TEXT, get_admin_menu())
        await call.answer()

    @dp.callback_query(F.data == "admin_cancel")
    async def admin_cancel(call: types.CallbackQuery, state: FSMContext):
        _reset_draft()
        await state.set_state(AdminState.menu)
        await _edit_or_answer(call, LANGUAGES["uz"]["admin_canceled"], get_admin_menu())
        await call.answer()

    # --- Добавление товара: шаг 1. Название ---

    @dp.callback_query(F.data == "admin_add")
    async def admin_add_start(call: types.CallbackQuery, state: FSMContext):
        _reset_draft()
        await state.set_state(AdminState.waiting_for_name)
        await _edit_or_answer(call, LANGUAGES["uz"]["admin_ask_name"], get_admin_cancel_keyboard())
        await call.answer()

    @dp.message(AdminState.waiting_for_name, F.text)
    async def admin_product_name(message: types.Message, state: FSMContext):
        new_product["name"] = message.text.strip()
        await state.set_state(AdminState.waiting_for_price)
        await message.answer(LANGUAGES["uz"]["admin_ask_price"], reply_markup=get_admin_cancel_keyboard())

    @dp.message(AdminState.waiting_for_name)
    async def admin_invalid_name(message: types.Message):
        await message.answer("⚠️ Iltimos, matn yuboring! / Отправьте текст!")

    # --- Шаг 2. Цена ---

    @dp.message(AdminState.waiting_for_price, F.text)
    async def admin_product_price(message: types.Message, state: FSMContext):
        raw = (
            message.text.strip()
            .replace(" ", "")
            .replace("so'm", "")
            .replace("сум", "")
            .replace("sum", "")
        )
        try:
            price = int(float(raw))
        except ValueError:
            await message.answer(LANGUAGES["uz"]["admin_invalid_price"])
            return

        new_product["price"] = price
        await state.set_state(AdminState.waiting_for_description)
        await message.answer(LANGUAGES["uz"]["admin_ask_desc"], reply_markup=get_admin_cancel_keyboard())

    @dp.message(AdminState.waiting_for_price)
    async def admin_invalid_price(message: types.Message):
        await message.answer(LANGUAGES["uz"]["admin_invalid_price"])

    # --- Шаг 3. Описание ---

    @dp.message(AdminState.waiting_for_description, F.text)
    async def admin_product_description(message: types.Message, state: FSMContext):
        new_product["description"] = " ".join(message.text.split())
        await state.set_state(AdminState.waiting_for_image)
        await message.answer(LANGUAGES["uz"]["admin_ask_image"], reply_markup=get_admin_skip_image_keyboard())

    @dp.message(AdminState.waiting_for_description)
    async def admin_invalid_desc(message: types.Message):
        await message.answer("⚠️ Iltimos, matn yuboring! / Отправьте текст!")

    # --- Шаг 4. Фото (загрузка или URL) ---

    @dp.message(AdminState.waiting_for_image, F.photo)
    async def admin_product_photo(message: types.Message, state: FSMContext):
        # Берём фото максимального размера и получаем прямую ссылку
        photo = message.photo[-1]
        file_info = await bot.get_file(photo.file_id)
        url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
        new_product["image"] = url
        await _ask_category(message, state)

    @dp.message(AdminState.waiting_for_image, F.text)
    async def admin_product_photo_url(message: types.Message, state: FSMContext):
        url = message.text.strip()
        if not url.lower().startswith(("http://", "https://")):
            await message.answer(
                "⚠️ Link http:// yoki https:// bilan boshlanishi kerak! / "
                "Ссылка должна начинаться с http(s)://"
            )
            return
        new_product["image"] = url
        await _ask_category(message, state)

    @dp.callback_query(AdminState.waiting_for_image, F.data == "adm_skip_image")
    async def admin_skip_image(call: types.CallbackQuery, state: FSMContext):
        new_product["image"] = ""
        await _ask_category(call.message, state)
        await call.answer()

    async def _ask_category(message: types.Message, state: FSMContext):
        await state.set_state(AdminState.waiting_for_category)
        await message.answer(
            LANGUAGES["uz"]["admin_ask_category"],
            reply_markup=get_admin_categories_keyboard(),
        )

    # --- Шаг 5. Категория и сохранение ---

    @dp.callback_query(AdminState.waiting_for_category, F.data.startswith("adm_cat_"))
    async def admin_choose_category(call: types.CallbackQuery, state: FSMContext):
        category = call.data.replace("adm_cat_", "")
        product = add_product(
            name=new_product.get("name", "Noma'lum"),
            price=new_product.get("price", 0),
            description=new_product.get("description", ""),
            image=new_product.get("image", ""),
            category=category,
        )
        lang = await get_lang(state)
        cat_title = CATEGORY_NAMES.get(category, {}).get(lang, category)
        await _edit_or_answer(
            call,
            LANGUAGES[lang]["admin_added"].format(
                name=_escape_html(product["name"]),
                price=format_price(product["price"]),
                category=cat_title,
            ),
            get_admin_menu(),
        )
        _reset_draft()
        await state.set_state(AdminState.menu)
        await call.answer("✅")

    # --- Список товаров ---

    @dp.callback_query(F.data == "admin_list")
    async def admin_list(call: types.CallbackQuery, state: FSMContext):
        lang = await get_lang(state)
        products = get_all_products()
        by_cat: dict = {}
        for p in products:
            by_cat.setdefault(p["category"], []).append(p)

        lines = ["📋 <b>Mahsulotlar ro'yxati / Список товаров:</b>"]
        for cat, items in by_cat.items():
            cat_title = CATEGORY_NAMES.get(cat, {}).get(lang, cat)
            lines.append(f"\n<b>{cat_title}</b>")
            for p in items:
                name = p["name"] if lang == "uz" else p.get("name_ru", p["name"])
                lines.append(f"  • {name} — {format_price(p['price'])}")

        text = "\n".join(lines)
        if len(text) > 4000:
            text = text[:4000] + "…"
        await state.set_state(AdminState.menu)
        await _edit_or_answer(call, text, get_admin_menu())
        await call.answer()

    # --- Редактирование товара ---

    @dp.callback_query(F.data == "admin_edit")
    async def admin_edit_start(call: types.CallbackQuery, state: FSMContext):
        if not _is_admin(call):
            await call.answer("⛔️", show_alert=True)
            return
        products = get_all_products()
        lang = await get_lang(state)
        if not products:
            await state.set_state(AdminState.menu)
            await _edit_or_answer(call, LANGUAGES[lang]["admin_edit_not_found"], get_admin_menu())
        else:
            await state.set_state(AdminState.waiting_for_edit_product)
            await _edit_or_answer(
                call,
                LANGUAGES[lang]["admin_edit_choose"],
                get_admin_products_keyboard(products, lang, action="edit"),
            )
        await call.answer()

    @dp.callback_query(AdminState.waiting_for_edit_product, F.data.startswith("adm_edit_"))
    async def admin_edit_select_product(call: types.CallbackQuery, state: FSMContext):
        if not _is_admin(call):
            await call.answer("⛔️", show_alert=True)
            return
        product_id = call.data[len("adm_edit_"):]
        product = get_product(product_id)
        lang = await get_lang(state)
        if not product:
            await _edit_or_answer(
                call,
                LANGUAGES[lang]["admin_edit_not_found"],
                get_admin_menu(),
            )
            await state.set_state(AdminState.menu)
            await call.answer()
            return

        await state.update_data(edit_product_id=product_id)
        await state.set_state(AdminState.waiting_for_edit_fields)
        name = product["name"] if lang == "uz" else product.get("name_ru", product["name"])
        await _edit_or_answer(
            call,
            LANGUAGES[lang]["admin_edit_fields"].format(name=_escape_html(name)),
            get_admin_edit_fields_keyboard(),
        )
        await call.answer()

    @dp.callback_query(AdminState.waiting_for_edit_fields, F.data.startswith("adm_edit_field_"))
    async def admin_edit_choose_field(call: types.CallbackQuery, state: FSMContext):
        if not _is_admin(call):
            await call.answer("⛔️", show_alert=True)
            return
        field = call.data[len("adm_edit_field_"):]
        data = await state.get_data()
        product = get_product(data.get("edit_product_id", ""))
        lang = await get_lang(state)
        if not product or field not in {
            "name", "name_ru", "price", "description", "description_ru", "image", "category"
        }:
            await call.answer(LANGUAGES[lang]["admin_edit_not_found"], show_alert=True)
            return

        if field == "category":
            await state.set_state(AdminState.waiting_for_edit_category)
            await _edit_or_answer(
                call,
                LANGUAGES[lang]["admin_edit_ask_category"],
                get_admin_edit_categories_keyboard(),
            )
        else:
            await state.update_data(edit_field=field)
            await state.set_state(AdminState.waiting_for_edit_value)
            prompts = {
                "name": "admin_edit_ask_name",
                "name_ru": "admin_edit_ask_name_ru",
                "price": "admin_edit_ask_price",
                "description": "admin_edit_ask_description",
                "description_ru": "admin_edit_ask_description_ru",
                "image": "admin_edit_ask_image",
            }
            markup = get_admin_edit_image_keyboard() if field == "image" else get_admin_cancel_keyboard()
            await _edit_or_answer(call, LANGUAGES[lang][prompts[field]], markup)
        await call.answer()

    async def save_edited_value(message: types.Message, state: FSMContext, field: str, value):
        data = await state.get_data()
        lang = await get_lang(state)
        product = update_product(data.get("edit_product_id", ""), {field: value})
        if not product:
            await state.set_state(AdminState.menu)
            await message.answer(LANGUAGES[lang]["admin_edit_not_found"], reply_markup=get_admin_menu())
            return
        await state.set_state(AdminState.waiting_for_edit_fields)
        name = product["name"] if lang == "uz" else product.get("name_ru", product["name"])
        await message.answer(
            f"{LANGUAGES[lang]['admin_edit_saved']}\n\n"
            f"{LANGUAGES[lang]['admin_edit_fields'].format(name=_escape_html(name))}",
            reply_markup=get_admin_edit_fields_keyboard(),
        )

    @dp.message(AdminState.waiting_for_edit_value, F.text)
    async def admin_edit_text_value(message: types.Message, state: FSMContext):
        data = await state.get_data()
        field = data.get("edit_field")
        value = message.text.strip()
        lang = await get_lang(state)
        if field == "price":
            raw = value.replace(" ", "").replace("so'm", "").replace("сум", "").replace("sum", "")
            try:
                value = int(float(raw))
            except ValueError:
                await message.answer(LANGUAGES[lang]["admin_invalid_price"])
                return
        elif field in {"description", "description_ru"}:
            value = " ".join(value.split())
        elif field == "image" and not value.lower().startswith(("http://", "https://")):
            await message.answer(LANGUAGES[lang]["admin_edit_invalid_image"])
            return
        elif field not in {"name", "name_ru", "description", "description_ru", "image"}:
            await message.answer(LANGUAGES[lang]["admin_edit_not_found"])
            return
        await save_edited_value(message, state, field, value)

    @dp.message(AdminState.waiting_for_edit_value, F.photo)
    async def admin_edit_photo(message: types.Message, state: FSMContext):
        data = await state.get_data()
        if data.get("edit_field") != "image":
            await message.answer(LANGUAGES[await get_lang(state)]["admin_edit_ask_image"])
            return
        photo = message.photo[-1]
        file_info = await bot.get_file(photo.file_id)
        url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
        await save_edited_value(message, state, "image", url)

    @dp.callback_query(AdminState.waiting_for_edit_category, F.data.startswith("adm_edit_cat_"))
    async def admin_edit_category(call: types.CallbackQuery, state: FSMContext):
        if not _is_admin(call):
            await call.answer("⛔️", show_alert=True)
            return
        category = call.data[len("adm_edit_cat_"):]
        data = await state.get_data()
        product = update_product(data.get("edit_product_id", ""), {"category": category})
        lang = await get_lang(state)
        if not product:
            await state.set_state(AdminState.menu)
            await _edit_or_answer(call, LANGUAGES[lang]["admin_edit_not_found"], get_admin_menu())
        else:
            await state.set_state(AdminState.waiting_for_edit_fields)
            name = product["name"] if lang == "uz" else product.get("name_ru", product["name"])
            await _edit_or_answer(
                call,
                f"{LANGUAGES[lang]['admin_edit_saved']}\n\n"
                f"{LANGUAGES[lang]['admin_edit_fields'].format(name=_escape_html(name))}",
                get_admin_edit_fields_keyboard(),
            )
        await call.answer()

    @dp.callback_query(F.data == "admin_edit_fields")
    async def admin_edit_fields_back(call: types.CallbackQuery, state: FSMContext):
        if not _is_admin(call):
            await call.answer("⛔️", show_alert=True)
            return
        data = await state.get_data()
        product = get_product(data.get("edit_product_id", ""))
        lang = await get_lang(state)
        if not product:
            await state.set_state(AdminState.menu)
            await _edit_or_answer(call, LANGUAGES[lang]["admin_edit_not_found"], get_admin_menu())
        else:
            await state.set_state(AdminState.waiting_for_edit_fields)
            name = product["name"] if lang == "uz" else product.get("name_ru", product["name"])
            await _edit_or_answer(
                call,
                LANGUAGES[lang]["admin_edit_fields"].format(name=_escape_html(name)),
                get_admin_edit_fields_keyboard(),
            )
        await call.answer()

    @dp.callback_query(F.data == "adm_edit_remove_image")
    async def admin_edit_remove_image(call: types.CallbackQuery, state: FSMContext):
        if not _is_admin(call):
            await call.answer("⛔️", show_alert=True)
            return
        data = await state.get_data()
        product = update_product(data.get("edit_product_id", ""), {"image": ""})
        lang = await get_lang(state)
        if not product:
            await state.set_state(AdminState.menu)
            await _edit_or_answer(call, LANGUAGES[lang]["admin_edit_not_found"], get_admin_menu())
        else:
            await state.set_state(AdminState.waiting_for_edit_fields)
            name = product["name"] if lang == "uz" else product.get("name_ru", product["name"])
            await _edit_or_answer(
                call,
                f"{LANGUAGES[lang]['admin_edit_saved']}\n\n"
                f"{LANGUAGES[lang]['admin_edit_fields'].format(name=_escape_html(name))}",
                get_admin_edit_fields_keyboard(),
            )
        await call.answer()

    # --- Удаление товара ---

    @dp.callback_query(F.data == "admin_delete")
    async def admin_delete_start(call: types.CallbackQuery, state: FSMContext):
        lang = await get_lang(state)
        # Удалять можно только товары, добавленные через админку
        base_ids = {str(p["id"]) for p in BASE_PRODUCTS}
        custom = [p for p in get_all_products() if str(p["id"]) not in base_ids]

        if not custom:
            await state.set_state(AdminState.menu)
            await _edit_or_answer(call, LANGUAGES[lang]["admin_nothing_to_delete"], get_admin_menu())
            await call.answer()
            return

        await state.set_state(AdminState.waiting_for_delete)
        await _edit_or_answer(call, LANGUAGES["uz"]["admin_delete_choose"], get_admin_products_keyboard(custom))
        await call.answer()

    @dp.callback_query(AdminState.waiting_for_delete, F.data.startswith("adm_del_"))
    async def admin_delete_confirm(call: types.CallbackQuery, state: FSMContext):
        product_id = call.data.replace("adm_del_", "")
        removed = delete_product(product_id)
        lang = await get_lang(state)

        if removed:
            name = removed["name"] if lang == "uz" else removed.get("name_ru", removed["name"])
            await _edit_or_answer(call, LANGUAGES[lang]["admin_deleted"].format(name=name), get_admin_menu())
        else:
            await _edit_or_answer(call, LANGUAGES[lang]["admin_nothing_to_delete"], get_admin_menu())

        await state.set_state(AdminState.menu)
        await call.answer()

    # --- Статистика ---

    @dp.callback_query(F.data == "admin_stats")
    async def admin_stats(call: types.CallbackQuery, state: FSMContext):
        all_products = get_all_products()
        base_ids = {str(p["id"]) for p in BASE_PRODUCTS}
        builtin = sum(1 for p in all_products if str(p["id"]) in base_ids)
        custom = len(all_products) - builtin
        lang = await get_lang(state)
        text = LANGUAGES[lang]["admin_stat_text"].format(
            total=len(all_products), builtin=builtin, custom=custom
        )
        await state.set_state(AdminState.menu)
        await _edit_or_answer(call, text, get_admin_menu())
        await call.answer()

    # --- Защита: не-админ в админ-состояниях ---

    @dp.message(AdminState.waiting_for_delete)
    async def admin_delete_fallback(message: types.Message, state: FSMContext):
        if not _is_admin(message):
            await state.clear()
            return
        await message.answer(LANGUAGES["uz"]["admin_delete_choose"])
