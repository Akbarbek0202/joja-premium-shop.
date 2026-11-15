import unittest

from bot.i18n import localized_product_field, to_uzbek_cyrillic
from bot.keyboards.reply import (
    CANCEL_ORDER_BUTTONS,
    CART_ADD_BUTTONS,
    CART_FINISH_BUTTONS,
    CONFIRM_ORDER_BUTTONS,
    LANGUAGE_BUTTONS,
    MAIN_ORDER_BUTTONS,
    get_cart_keyboard,
    get_confirm_keyboard,
    get_main_keyboard,
)
from bot.locales import CATEGORY_NAMES, LANGUAGES


class UzbekCyrillicTests(unittest.TestCase):
    def test_transliterates_uzbek_digraphs_and_apostrophes(self):
        self.assertEqual(
            to_uzbek_cyrillic("O'zbekcha, Shirin jo'ja: g'oz, so'm"),
            "Ўзбекча, Ширин жўжа: ғоз, сўм",
        )

    def test_preserves_html_tags_in_translated_bot_messages(self):
        self.assertEqual(
            to_uzbek_cyrillic("<b>{product}</b> uchun {qty} dona"),
            "<b>{product}</b> учун {qty} дона",
        )
        self.assertIn("{product}", LANGUAGES["uz_cyrl"]["ask_qty"])
        self.assertIn("Жўжа", LANGUAGES["uz_cyrl"]["ask_qty"].format(product="Жўжа"))

    def test_language_catalogs_include_all_three_choices(self):
        self.assertEqual(set(LANGUAGES), {"uz", "uz_cyrl", "ru"})
        self.assertTrue(all("uz_cyrl" in names for names in CATEGORY_NAMES.values()))
        product = {"name": "Jo'ja", "name_ru": "Цыплёнок"}
        self.assertEqual(localized_product_field(product, "name", "uz_cyrl"), "Жўжа")
        self.assertEqual(localized_product_field(product, "name", "ru"), "Цыплёнок")

    def test_cyrillic_bot_buttons_match_order_handlers(self):
        self.assertEqual(set(LANGUAGE_BUTTONS), {"uz", "uz_cyrl", "ru"})
        self.assertIn(get_main_keyboard("uz_cyrl").keyboard[1][0].text, MAIN_ORDER_BUTTONS)
        cart_keyboard = get_cart_keyboard("uz_cyrl")
        self.assertIn(cart_keyboard.keyboard[0][0].text, CART_ADD_BUTTONS)
        self.assertIn(cart_keyboard.keyboard[1][0].text, CART_FINISH_BUTTONS)
        confirm_keyboard = get_confirm_keyboard("uz_cyrl")
        self.assertIn(confirm_keyboard.keyboard[0][0].text, CONFIRM_ORDER_BUTTONS)
        self.assertIn(confirm_keyboard.keyboard[1][0].text, CANCEL_ORDER_BUTTONS)


if __name__ == "__main__":
    unittest.main()
