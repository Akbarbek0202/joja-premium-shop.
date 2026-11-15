from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.i18n import localized_product_field, to_uzbek_cyrillic
from bot.locales import CATEGORY_NAMES


def _trilingual(uzbek: str, russian: str) -> str:
    return f"{uzbek} / {to_uzbek_cyrillic(uzbek)} / {russian}"


def get_admin_menu() -> InlineKeyboardMarkup:
    """Главное меню админ-панели."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_trilingual("Mahsulot qo'shish", "Добавить товар"), callback_data="admin_add")],
            [InlineKeyboardButton(text=_trilingual("Ro'yxat", "Список"), callback_data="admin_list")],
            [InlineKeyboardButton(text=_trilingual("Tahrirlash", "Редактировать"), callback_data="admin_edit")],
            [InlineKeyboardButton(text=_trilingual("O'chirish", "Удалить"), callback_data="admin_delete")],
            [InlineKeyboardButton(text=_trilingual("Statistika", "Статистика"), callback_data="admin_stats")],
        ]
    )


def get_admin_categories_keyboard() -> InlineKeyboardMarkup:
    """Выбор категории для нового товара."""
    rows = []
    row = []
    for cat, names in CATEGORY_NAMES.items():
        title = f"{names['uz']} / {names['uz_cyrl']} / {names['ru']}"
        row.append(InlineKeyboardButton(text=title, callback_data=f"adm_cat_{cat}"))
        if len(row) == 1:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([InlineKeyboardButton(text="❌ " + _trilingual("Bekor qilish", "Отмена"), callback_data="admin_cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_admin_products_keyboard(products: list, lang: str = "uz", action: str = "delete") -> InlineKeyboardMarkup:
    """Список товаров для выбора действия."""
    rows = []
    callback_prefix = "adm_edit_" if action == "edit" else "adm_del_"
    for p in products:
        name = localized_product_field(p, "name", lang)
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"{'✏️' if action == 'edit' else '🗑'} {name} — {p['price']}",
                    callback_data=f"{callback_prefix}{p['id']}",
                )
            ]
        )
    rows.append([InlineKeyboardButton(text="⬅️ " + _trilingual("Orqaga", "Назад"), callback_data="admin_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_admin_edit_fields_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 " + _trilingual("Nomi", "Название"), callback_data="adm_edit_field_name")],
            [InlineKeyboardButton(text="📝 " + _trilingual("Ruscha nomi", "Название RU"), callback_data="adm_edit_field_name_ru")],
            [InlineKeyboardButton(text="💰 " + _trilingual("Narxi", "Цена"), callback_data="adm_edit_field_price")],
            [InlineKeyboardButton(text="📄 " + _trilingual("Tavsif", "Описание"), callback_data="adm_edit_field_description")],
            [InlineKeyboardButton(text="📄 " + _trilingual("Ruscha tavsifi", "Описание RU"), callback_data="adm_edit_field_description_ru")],
            [InlineKeyboardButton(text="🖼 " + _trilingual("Rasm", "Фото"), callback_data="adm_edit_field_image")],
            [InlineKeyboardButton(text="📂 " + _trilingual("Kategoriya", "Категория"), callback_data="adm_edit_field_category")],
            [InlineKeyboardButton(text="⬅️ " + _trilingual("Orqaga", "Назад"), callback_data="admin_menu")],
        ]
    )


def get_admin_edit_categories_keyboard() -> InlineKeyboardMarkup:
    rows = []
    for cat, names in CATEGORY_NAMES.items():
        title = f"{names['uz']} / {names['uz_cyrl']} / {names['ru']}"
        rows.append([InlineKeyboardButton(text=title, callback_data=f"adm_edit_cat_{cat}")])
    rows.append([InlineKeyboardButton(text="⬅️ " + _trilingual("Orqaga", "Назад"), callback_data="admin_edit_fields")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_admin_edit_image_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🗑 " + _trilingual("Rasmni o'chirish", "Удалить фото"), callback_data="adm_edit_remove_image")],
            [InlineKeyboardButton(text="⬅️ " + _trilingual("Orqaga", "Назад"), callback_data="admin_edit_fields")],
        ]
    )


def get_admin_skip_image_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⏭ " + _trilingual("O'tkazib yuborish", "Пропустить"),
                    callback_data="adm_skip_image",
                )
            ]
        ]
    )


def get_admin_cancel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌ " + _trilingual("Bekor qilish", "Отмена"),
                    callback_data="admin_cancel",
                )
            ]
        ]
    )
