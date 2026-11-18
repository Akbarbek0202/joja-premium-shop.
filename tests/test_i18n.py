import unittest
import unicodedata

from bot.catalog_data import BASE_PRODUCTS
from bot.i18n import localized_product_field
from bot.keyboards.admin import (
    get_admin_categories_keyboard,
    get_admin_menu,
)
from bot.keyboards.inline import (
    get_categories_keyboard,
    get_category_products_keyboard,
)
from bot.keyboards.reply import (
    get_cart_keyboard,
    get_confirm_keyboard,
    get_main_keyboard,
)
from bot.keyboards.admin import get_admin_products_keyboard
from bot.locales import CATEGORY_NAMES, LANGUAGES


class RussianOnlyTests(unittest.TestCase):
    def test_only_russian_locale_is_available(self):
        self.assertEqual(set(LANGUAGES), {"ru"})
        self.assertTrue(all(isinstance(name, str) for name in CATEGORY_NAMES.values()))
        self.assertTrue(all(product.get("name_ru") for product in BASE_PRODUCTS))
        self.assertTrue(all(product.get("description_ru") for product in BASE_PRODUCTS))

    def test_product_fields_resolve_to_russian_catalog_values(self):
        product = {"name": "Boldir \U0001f357", "name_ru": "Голень \U0001f357"}
        self.assertEqual(localized_product_field(product, "name"), "Голень")
        self.assertEqual(localized_product_field({"name": "Голень \U0001f357"}, "name"), "Голень")
        self.assertEqual(localized_product_field({"name": "Boldir \U0001f357"}, "name"), "")

    def test_all_bot_keyboards_use_russian_labels(self):
        keyboards = (
            get_main_keyboard(),
            get_cart_keyboard(),
            get_confirm_keyboard(),
        )
        labels = [
            button.text
            for keyboard in keyboards
            for row in keyboard.keyboard
            for button in row
        ]
        labels.extend(
            button.text
            for keyboard in (
                get_admin_menu(),
                get_admin_categories_keyboard(),
                get_admin_products_keyboard(BASE_PRODUCTS, action="edit"),
                get_categories_keyboard(),
                get_category_products_keyboard("parts"),
            )
            for row in keyboard.inline_keyboard
            for button in row
        )

        self.assertIn("Сделать заказ", labels)
        self.assertIn("Завершить заказ", labels)
        self.assertIn("Да, подтверждаю", labels)
        self.assertFalse(any("O'zbekcha" in label or "Buyurtma" in label for label in labels))
        category_names = set(CATEGORY_NAMES.values())
        self.assertTrue(
            all(
                label in category_names
                or not any(
                    unicodedata.category(character) in {"So", "Sk", "Me"}
                    for character in label
                )
                for label in labels
            )
        )


if __name__ == "__main__":
    unittest.main()
