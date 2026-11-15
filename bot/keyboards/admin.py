from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.locales import CATEGORY_NAMES


def get_admin_menu() -> InlineKeyboardMarkup:
    """Главное меню админ-панели."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Mahsulot qo'shish / Добавить товар", callback_data="admin_add")],
            [InlineKeyboardButton(text="📋 Ro'yxat / Список", callback_data="admin_list")],
            [InlineKeyboardButton(text="✏️ Tahrirlash / Редактировать", callback_data="admin_edit")],
            [InlineKeyboardButton(text="🗑 O'chirish / Удалить", callback_data="admin_delete")],
            [InlineKeyboardButton(text="📊 Statistika / Статистика", callback_data="admin_stats")],
        ]
    )


def get_admin_categories_keyboard() -> InlineKeyboardMarkup:
    """Выбор категории для нового товара."""
    rows = []
    row = []
    for cat, names in CATEGORY_NAMES.items():
        title = f"{names['uz']} / {names['ru']}"
        row.append(InlineKeyboardButton(text=title, callback_data=f"adm_cat_{cat}"))
        if len(row) == 1:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([InlineKeyboardButton(text="❌ Bekor qilish / Отмена", callback_data="admin_cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_admin_products_keyboard(products: list, lang: str = "uz", action: str = "delete") -> InlineKeyboardMarkup:
    """Список товаров для выбора действия."""
    rows = []
    callback_prefix = "adm_edit_" if action == "edit" else "adm_del_"
    for p in products:
        name = p["name"] if lang == "uz" else p.get("name_ru", p["name"])
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"{'✏️' if action == 'edit' else '🗑'} {name} — {p['price']}",
                    callback_data=f"{callback_prefix}{p['id']}",
                )
            ]
        )
    rows.append([InlineKeyboardButton(text="⬅️ Orqaga / Назад", callback_data="admin_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_admin_edit_fields_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Название / Nomi", callback_data="adm_edit_field_name")],
            [InlineKeyboardButton(text="📝 Название RU / Ruscha nomi", callback_data="adm_edit_field_name_ru")],
            [InlineKeyboardButton(text="💰 Цена / Narxi", callback_data="adm_edit_field_price")],
            [InlineKeyboardButton(text="📄 Описание / Tavsif", callback_data="adm_edit_field_description")],
            [InlineKeyboardButton(text="📄 Описание RU / Ruscha tavsifi", callback_data="adm_edit_field_description_ru")],
            [InlineKeyboardButton(text="🖼 Фото / Rasm", callback_data="adm_edit_field_image")],
            [InlineKeyboardButton(text="📂 Категория / Kategoriya", callback_data="adm_edit_field_category")],
            [InlineKeyboardButton(text="⬅️ Назад / Orqaga", callback_data="admin_menu")],
        ]
    )


def get_admin_edit_categories_keyboard() -> InlineKeyboardMarkup:
    rows = []
    for cat, names in CATEGORY_NAMES.items():
        title = f"{names['uz']} / {names['ru']}"
        rows.append([InlineKeyboardButton(text=title, callback_data=f"adm_edit_cat_{cat}")])
    rows.append([InlineKeyboardButton(text="⬅️ Назад / Orqaga", callback_data="admin_edit_fields")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_admin_edit_image_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Удалить фото / Rasmni o'chirish", callback_data="adm_edit_remove_image")],
            [InlineKeyboardButton(text="⬅️ Назад / Orqaga", callback_data="admin_edit_fields")],
        ]
    )


def get_admin_skip_image_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⏭ Skip / Пропустить", callback_data="adm_skip_image")]]
    )


def get_admin_cancel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌ Bekor qilish / Отмена", callback_data="admin_cancel")]])
