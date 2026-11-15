from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.services.catalog import CATEGORIES, get_products_by_category
from bot.locales import CATEGORY_NAMES
from bot.i18n import localized_product_field


def get_categories_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    rows = []
    row: list = []
    for category in CATEGORIES:
        row.append(
            InlineKeyboardButton(
                text=CATEGORY_NAMES.get(category, category),
                callback_data=f"menu_cat_{category}",
            )
        )
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_category_products_keyboard(category: str, lang: str = "ru") -> InlineKeyboardMarkup:
    products = get_products_by_category(category)
    if not products:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ К категориям", callback_data="to_categories")]
            ]
        )

    rows = []
    row: list = []
    for product in products:
        name = localized_product_field(product, "name") or "Товар"
        row.append(
            InlineKeyboardButton(text=name, callback_data=f"cat_{product['id']}")
        )
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append(
        [InlineKeyboardButton(text="⬅️ К категориям", callback_data="to_categories")]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_quantity_keyboard(quantity: int, lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➖", callback_data="qty_minus"),
                InlineKeyboardButton(text=f"{quantity} шт.", callback_data="qty_count"),
                InlineKeyboardButton(text="➕", callback_data="qty_plus"),
            ],
            [
                InlineKeyboardButton(
                    text="📥 Добавить в корзину", callback_data="qty_confirm"
                )
            ],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="qty_back")],
        ]
    )


def get_product_back_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="to_categories")]
        ]
    )
