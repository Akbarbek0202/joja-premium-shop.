from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.services.catalog import CATEGORIES, get_products_by_category
from bot.locales import CATEGORY_NAMES


def get_categories_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Меню категорий (динамически из каталога)."""
    rows = []
    row: list = []
    for cat in CATEGORIES:
        title = CATEGORY_NAMES.get(cat, {}).get(lang, cat)
        row.append(InlineKeyboardButton(text=title, callback_data=f"menu_cat_{cat}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)

    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_category_products_keyboard(category: str, lang: str) -> InlineKeyboardMarkup:
    """Список товаров категории (динамически из каталога)."""
    products = get_products_by_category(category)

    if not products:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ " + ("Menuga qaytish" if lang == "uz" else "К категориям"), callback_data="to_categories")]
            ]
        )

    # По 2 кнопки в ряд
    rows = []
    row: list = []
    for p in products:
        name = p["name"] if lang == "uz" else p.get("name_ru", p["name"])
        row.append(InlineKeyboardButton(text=name, callback_data=f"cat_{p['id']}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)

    rows.append(
        [
            InlineKeyboardButton(
                text="⬅️ " + ("Menuga qaytish" if lang == "uz" else "К категориям"),
                callback_data="to_categories",
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_quantity_keyboard(quantity: int, lang: str = "uz") -> InlineKeyboardMarkup:
    """Клавиатура выбора количества."""
    is_uz = lang == "uz"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➖", callback_data="qty_minus"),
                InlineKeyboardButton(
                    text=("dona" if is_uz else "шт") if quantity is None else f"{quantity} {'dona' if is_uz else 'шт'}",
                    callback_data="qty_count",
                ),
                InlineKeyboardButton(text="➕", callback_data="qty_plus"),
            ],
            [
                InlineKeyboardButton(
                    text="📥 Savatga qo'shish" if is_uz else "📥 Добавить в корзину",
                    callback_data="qty_confirm",
                )
            ],
            [
                InlineKeyboardButton(text="⬅️ Orqaga" if is_uz else "⬅️ Назад", callback_data="qty_back")
            ],
        ]
    )


def get_product_back_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Возврат к списку товаров категории после просмотра карточки с фото."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ " + ("Orqaga" if lang == "uz" else "Назад"),
                    callback_data="to_categories",
                )
            ]
        ]
    )



