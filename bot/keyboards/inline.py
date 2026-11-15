from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.services.catalog import CATEGORIES, get_products_by_category
from bot.i18n import localized_product_field, to_uzbek_cyrillic
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
                [
                    InlineKeyboardButton(
                        text="⬅️ "
                        + (
                            "К категориям"
                            if lang == "ru"
                            else to_uzbek_cyrillic("Menuga qaytish")
                            if lang == "uz_cyrl"
                            else "Menuga qaytish"
                        ),
                        callback_data="to_categories",
                    )
                ]
            ]
        )

    # По 2 кнопки в ряд
    rows = []
    row: list = []
    for p in products:
        name = localized_product_field(p, "name", lang)
        row.append(InlineKeyboardButton(text=name, callback_data=f"cat_{p['id']}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)

    rows.append(
        [
            InlineKeyboardButton(
                text="⬅️ "
                + (
                    "К категориям"
                    if lang == "ru"
                    else to_uzbek_cyrillic("Menuga qaytish")
                    if lang == "uz_cyrl"
                    else "Menuga qaytish"
                ),
                callback_data="to_categories",
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_quantity_keyboard(quantity: int, lang: str = "uz") -> InlineKeyboardMarkup:
    """Клавиатура выбора количества."""
    is_ru = lang == "ru"
    uz_text = to_uzbek_cyrillic if lang == "uz_cyrl" else lambda text: text
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➖", callback_data="qty_minus"),
                InlineKeyboardButton(
                    text=("шт" if is_ru else uz_text("dona"))
                    if quantity is None
                    else f"{quantity} {'шт' if is_ru else uz_text('dona')}",
                    callback_data="qty_count",
                ),
                InlineKeyboardButton(text="➕", callback_data="qty_plus"),
            ],
            [
                InlineKeyboardButton(
                    text="📥 Добавить в корзину"
                    if is_ru
                    else "📥 " + uz_text("Savatga qo'shish"),
                    callback_data="qty_confirm",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад"
                    if is_ru
                    else f"⬅️ {uz_text('Orqaga')}",
                    callback_data="qty_back",
                )
            ],
        ]
    )


def get_product_back_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Возврат к списку товаров категории после просмотра карточки с фото."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ "
                    + (
                        "Назад"
                        if lang == "ru"
                        else to_uzbek_cyrillic("Orqaga")
                        if lang == "uz_cyrl"
                        else "Orqaga"
                    ),
                    callback_data="to_categories",
                )
            ]
        ]
    )



