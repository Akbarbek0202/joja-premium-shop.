from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.locales import CATEGORY_NAMES
from bot.i18n import localized_product_field


def get_admin_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить товар", callback_data="admin_add")],
            [InlineKeyboardButton(text="📋 Список товаров", callback_data="admin_list")],
            [InlineKeyboardButton(text="✏️ Редактировать товар", callback_data="admin_edit")],
            [InlineKeyboardButton(text="🗑 Удалить товар", callback_data="admin_delete")],
            [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        ]
    )


def get_admin_categories_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=name, callback_data=f"adm_cat_{category}")]
        for category, name in CATEGORY_NAMES.items()
    ]
    rows.append([InlineKeyboardButton(text="❌ Отмена", callback_data="admin_cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_admin_products_keyboard(
    products: list, lang: str = "ru", action: str = "delete"
) -> InlineKeyboardMarkup:
    callback_prefix = "adm_edit_" if action == "edit" else "adm_del_"
    rows = [
        [
            InlineKeyboardButton(
                text=f"{'✏️' if action == 'edit' else '🗑'} "
                f"{localized_product_field(product, 'name') or 'Товар'} — {product['price']}",
                callback_data=f"{callback_prefix}{product['id']}",
            )
        ]
        for product in products
    ]
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_admin_edit_fields_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Название", callback_data="adm_edit_field_name_ru")],
            [InlineKeyboardButton(text="💰 Цена", callback_data="adm_edit_field_price")],
            [InlineKeyboardButton(text="📄 Описание", callback_data="adm_edit_field_description_ru")],
            [InlineKeyboardButton(text="🖼 Фото", callback_data="adm_edit_field_image")],
            [InlineKeyboardButton(text="📂 Категория", callback_data="adm_edit_field_category")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_menu")],
        ]
    )


def get_admin_edit_categories_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=name, callback_data=f"adm_edit_cat_{category}")]
        for category, name in CATEGORY_NAMES.items()
    ]
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_edit_fields")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_admin_edit_image_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Удалить фото", callback_data="adm_edit_remove_image")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_edit_fields")],
        ]
    )


def get_admin_skip_image_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏭ Пропустить", callback_data="adm_skip_image")]
        ]
    )


def get_admin_cancel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="admin_cancel")]
        ]
    )
