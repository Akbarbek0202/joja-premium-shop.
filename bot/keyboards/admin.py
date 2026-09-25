from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.locales import CATEGORY_NAMES


def get_admin_menu() -> InlineKeyboardMarkup:
    """Главное меню админ-панели."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Mahsulot qo'shish / Добавить товар", callback_data="admin_add")],
            [InlineKeyboardButton(text="📋 Ro'yxat / Список", callback_data="admin_list")],
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


def get_admin_products_keyboard(products: list, lang: str = "uz") -> InlineKeyboardMarkup:
    """Список товаров для удаления (только те, что добавлены папой)."""
    rows = []
    for p in products:
        name = p["name"] if lang == "uz" else p.get("name_ru", p["name"])
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"🗑 {name} — {p['price']}",
                    callback_data=f"adm_del_{p['id']}",
                )
            ]
        )
    rows.append([InlineKeyboardButton(text="⬅️ Orqaga / Назад", callback_data="admin_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_admin_skip_image_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⏭ Skip / Пропустить", callback_data="adm_skip_image")]]
    )


def get_admin_cancel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌ Bekor qilish / Отмена", callback_data="admin_cancel")]])
