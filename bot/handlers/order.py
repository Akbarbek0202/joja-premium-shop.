import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest, TelegramNotFound

from bot.keyboards.inline import (
    get_categories_keyboard,
    get_category_products_keyboard,
    get_quantity_keyboard,
)
from bot.keyboards.reply import (
    get_cart_keyboard,
    get_confirm_keyboard,
    get_contact_keyboard,
    get_location_keyboard,
    get_main_keyboard,
)
from bot.locales import LANGUAGES
from bot.services.catalog import get_product, format_price
from bot.services.photo_cache import send_product_photo
from bot.states import OrderState
from bot.utils import get_lang, format_cart_summary

logger = logging.getLogger(__name__)


def _card_text(product: dict, lang: str) -> str:
    """Текст карточки товара."""
    if lang == "uz":
        name = product["name"]
        description = product.get("description", "")
        return (
            f"🍗 <b>{name}</b>\n\n"
            f"💰 Narxi: {format_price(product['price'])} so'm\n\n"
            f"📝 {description}\n\n"
            f"Kattaligini/sonini tanlang:"
        )
    name = product.get("name_ru", product["name"])
    description = product.get("description_ru", product.get("description", ""))
    return (
        f"🍗 <b>{name}</b>\n\n"
        f"💰 Цена: {format_price(product['price'])} сум\n\n"
        f"📝 {description}\n\n"
        f"Выберите количество:"
    )


def register_handlers(dp: Dispatcher, bot: Bot) -> None:
    # --- Начало заказа ---

    @dp.message(F.text.in_({"📦 Buyurtma berish", "📦 Сделать заказ"}))
    async def start_order(message: types.Message, state: FSMContext):
        lang = await get_lang(state)
        await state.update_data(cart={}, from_webapp=False)
        await state.set_state(OrderState.waiting_for_store_name)
        await message.answer(
            LANGUAGES[lang]["ask_store"],
            reply_markup=types.ReplyKeyboardRemove(),
        )

    @dp.message(OrderState.waiting_for_store_name, F.text)
    async def process_store_name(message: types.Message, state: FSMContext):
        lang = await get_lang(state)
        data = await state.get_data()
        await state.update_data(store_name=message.text)

        if data.get("from_webapp"):
            # После веб-приложения товары уже в корзине — сразу адрес
            markup = get_location_keyboard(lang)
            await message.answer(LANGUAGES[lang]["ask_location"], reply_markup=markup)
            await state.set_state(OrderState.waiting_for_address)
        else:
            await state.set_state(OrderState.waiting_for_product)
            await message.answer(
                LANGUAGES[lang]["select_category"],
                reply_markup=get_categories_keyboard(lang),
            )

    @dp.message(OrderState.waiting_for_store_name)
    async def invalid_store_name(message: types.Message, state: FSMContext):
        lang = await get_lang(state)
        await message.answer(LANGUAGES[lang]["invalid_store"])

    # --- Каталог ---

    @dp.callback_query(OrderState.waiting_for_product, F.data.startswith("menu_cat_"))
    async def open_category(call: types.CallbackQuery, state: FSMContext):
        lang = await get_lang(state)
        cat_name = call.data.replace("menu_cat_", "")

        text = LANGUAGES[lang]["select_product"]
        keyboard = get_category_products_keyboard(category=cat_name, lang=lang)

        try:
            await call.message.edit_text(text, reply_markup=keyboard)
        except (TelegramBadRequest, TelegramNotFound):
            await call.message.answer(text, reply_markup=keyboard)
        await call.answer()

    @dp.callback_query(OrderState.waiting_for_product, F.data == "to_categories")
    async def back_to_categories(call: types.CallbackQuery, state: FSMContext):
        lang = await get_lang(state)
        text = LANGUAGES[lang]["select_category"]
        keyboard = get_categories_keyboard(lang)

        try:
            await call.message.edit_text(text, reply_markup=keyboard)
        except (TelegramBadRequest, TelegramNotFound):
            await call.message.answer(text, reply_markup=keyboard)
        await call.answer()

    # --- Выбор товара: карточка с фото ---

    @dp.callback_query(OrderState.waiting_for_product, F.data.startswith("cat_"))
    async def select_product(call: types.CallbackQuery, state: FSMContext):
        lang = await get_lang(state)
        product_id = call.data.replace("cat_", "")
        product = get_product(product_id)
        if not product:
            await call.answer("Mahsulot topilmadi" if lang == "uz" else "Товар не найден", show_alert=True)
            return

        await state.update_data(current_product_id=product_id, current_qty=1)

        text = _card_text(product, lang)
        keyboard = get_quantity_keyboard(1, lang)

        if product.get("image"):
            # Карточка с фото: удаляем список и присылаем фото с описанием
            try:
                await call.message.delete()
            except (TelegramBadRequest, TelegramNotFound):
                pass
            try:
                await send_product_photo(bot, call.message.chat.id, product["image"], text, keyboard)
            except (TelegramBadRequest, TelegramNotFound) as e:
                # Фото не загрузилось (битая ссылка) — отправляем текстом
                logger.warning(f"Не удалось отправить фото {product['image']}: {e}")
                await call.message.answer(text, reply_markup=keyboard)
        else:
            # Без фото — просто редактируем сообщение
            try:
                await call.message.edit_text(text, reply_markup=keyboard)
            except (TelegramBadRequest, TelegramNotFound):
                await call.message.answer(text, reply_markup=keyboard)

        await state.set_state(OrderState.waiting_for_quantity)
        await call.answer()

    # --- Выбор количества ---

    @dp.callback_query(OrderState.waiting_for_quantity, F.data.in_({"qty_plus", "qty_minus"}))
    async def change_quantity(call: types.CallbackQuery, state: FSMContext):
        lang = await get_lang(state)
        data = await state.get_data()

        current_qty = data.get("current_qty", 1)
        product_id = str(data.get("current_product_id"))
        product = get_product(product_id)
        if not product:
            await call.answer("Mahsulot topilmadi" if lang == "uz" else "Товар не найден", show_alert=True)
            return

        if call.data == "qty_plus":
            current_qty += 1
        elif call.data == "qty_minus" and current_qty > 1:
            current_qty -= 1

        await state.update_data(current_qty=current_qty)

        text = _card_text(product, lang)
        keyboard = get_quantity_keyboard(current_qty, lang)

        # Если карточка с фото — редактируем caption, иначе текст
        if call.message.photo:
            try:
                await call.message.edit_caption(caption=text, reply_markup=keyboard)
            except (TelegramBadRequest, TelegramNotFound):
                pass
        else:
            try:
                await call.message.edit_text(text, reply_markup=keyboard)
            except (TelegramBadRequest, TelegramNotFound):
                pass

        await call.answer()

    @dp.callback_query(OrderState.waiting_for_quantity, F.data == "qty_confirm")
    async def confirm_quantity(call: types.CallbackQuery, state: FSMContext):
        lang = await get_lang(state)
        data = await state.get_data()

        product_id = str(data.get("current_product_id"))
        current_qty = int(data.get("current_qty", 1))
        cart = data.get("cart", {})

        if product_id in cart:
            if isinstance(cart[product_id], dict):
                cart[product_id]["quantity"] += current_qty
            else:
                cart[product_id] = int(cart[product_id]) + current_qty
        else:
            cart[product_id] = current_qty

        await state.update_data(cart=cart)

        total_label = "Jami" if lang == "uz" else "Итого"
        currency = "so'm" if lang == "uz" else "сум"

        cart_text = LANGUAGES[lang]["cart_title"]
        products_list, total_sum = format_cart_summary(cart, lang)
        cart_text += products_list
        cart_text += f"\n💰 <b>{total_label}: {format_price(total_sum)} {currency}</b>\n"
        cart_text += LANGUAGES[lang]["cart_footer"]

        try:
            await call.message.delete()
        except (TelegramBadRequest, TelegramNotFound):
            pass

        await call.message.answer(cart_text, reply_markup=get_cart_keyboard(lang))
        await state.set_state(OrderState.waiting_for_cart)
        await call.answer()

    @dp.callback_query(OrderState.waiting_for_quantity, F.data == "qty_back")
    async def back_from_quantity(call: types.CallbackQuery, state: FSMContext):
        lang = await get_lang(state)
        await state.set_state(OrderState.waiting_for_product)

        text = LANGUAGES[lang]["select_category"]
        keyboard = get_categories_keyboard(lang)

        try:
            await call.message.delete()
        except (TelegramBadRequest, TelegramNotFound):
            pass
        await call.message.answer(text, reply_markup=keyboard)
        await call.answer()

    # --- Корзина ---

    @dp.message(OrderState.waiting_for_cart, F.text.in_({"➕ Yana mahsulot qo'shish", "➕ Добавить ещё товар"}))
    async def add_more(message: types.Message, state: FSMContext):
        lang = await get_lang(state)
        await state.set_state(OrderState.waiting_for_product)
        await message.answer(
            LANGUAGES[lang]["select_category"],
            reply_markup=get_categories_keyboard(lang),
        )

    @dp.message(OrderState.waiting_for_cart, F.text.in_({"✅ Buyurtmani yakunlash", "✅ Завершить заказ"}))
    async def finish_order(message: types.Message, state: FSMContext):
        lang = await get_lang(state)
        await message.answer(LANGUAGES[lang]["ask_location"], reply_markup=get_location_keyboard(lang))
        await state.set_state(OrderState.waiting_for_address)

    # --- Адрес ---

    @dp.message(OrderState.waiting_for_address, F.location)
    async def process_location(message: types.Message, state: FSMContext):
        try:
            lang = await get_lang(state)
            lat = message.location.latitude
            lon = message.location.longitude
            await state.update_data(lat=lat, lon=lon)

            await message.answer(LANGUAGES[lang]["ask_contact"], reply_markup=get_contact_keyboard(lang))
            await state.set_state(OrderState.waiting_for_contact)
        except Exception:
            # Даже при ошибке не оставляем пользователя без ответа
            logger.exception("process_location xatosi")
            await message.answer(LANGUAGES["ru"]["ask_contact"], reply_markup=get_contact_keyboard("ru"))
            await state.set_state(OrderState.waiting_for_contact)

    @dp.message(OrderState.waiting_for_address)
    async def invalid_location(message: types.Message, state: FSMContext):
        lang = await get_lang(state)
        await message.answer(LANGUAGES[lang]["invalid_location"], reply_markup=get_location_keyboard(lang))

    # --- Контакт ---

    @dp.message(OrderState.waiting_for_contact, F.contact)
    async def process_contact(message: types.Message, state: FSMContext):
        lang = await get_lang(state)
        phone = message.contact.phone_number
        await state.update_data(contact=phone)

        data = await state.get_data()
        store_name = data.get("store_name")
        cart = data.get("cart", {})

        products_list, total_sum = format_cart_summary(cart, lang)
        total_label = "Jami summa" if lang == "uz" else "Итоговая сумма"
        currency = "so'm" if lang == "uz" else "сум"
        products_list += f"\n💰 <b>{total_label}: {format_price(total_sum)} {currency}</b>"

        checkout_text = LANGUAGES[lang]["checkout"].format(
            name="",
            store=store_name,
            products=products_list,
            phone=phone,
        )
        await message.answer(checkout_text, reply_markup=get_confirm_keyboard(lang))
        await state.set_state(OrderState.waiting_for_confirmation)

    @dp.message(OrderState.waiting_for_contact)
    async def invalid_contact(message: types.Message, state: FSMContext):
        lang = await get_lang(state)
        await message.answer(LANGUAGES[lang]["invalid_contact"], reply_markup=get_contact_keyboard(lang))

    # --- Подтверждение ---

    @dp.message(OrderState.waiting_for_confirmation, F.text.in_({"Ha, tasdiqlayman", "Да, подтверждаю"}))
    async def confirm_order(message: types.Message, state: FSMContext):
        from bot.handlers.notify import send_order_notification

        lang = await get_lang(state)
        data = await state.get_data()

        ok = await send_order_notification(
            bot=bot,
            data=data,
            lang=lang,
        )

        if not ok:
            logger.error("Не удалось отправить заказ админу")
        await message.answer(LANGUAGES[lang]["success"], reply_markup=get_main_keyboard(lang))
        await state.clear()

    @dp.message(OrderState.waiting_for_confirmation, F.text.in_({"Bekor qilish", "Отменить"}))
    async def cancel_order(message: types.Message, state: FSMContext):
        lang = await get_lang(state)
        await message.answer(LANGUAGES[lang]["canceled"], reply_markup=get_main_keyboard(lang))
        await state.clear()
