from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

from bot.config import WEBAPP_URL
from bot.i18n import to_uzbek_cyrillic


LANGUAGE_BUTTONS = {
    "uz": "O'zbekcha (lotin) 🇺🇿",
    "uz_cyrl": "Ўзбекча (кирилл) 🇺🇿",
    "ru": "Русский 🇷🇺",
}
MAIN_ORDER_BUTTONS = {
    "📦 Buyurtma berish",
    f"📦 {to_uzbek_cyrillic('Buyurtma berish')}",
    "📦 Сделать заказ",
}
CART_ADD_BUTTONS = {
    "➕ Yana mahsulot qo'shish",
    "➕ " + to_uzbek_cyrillic("Yana mahsulot qo'shish"),
    "➕ Добавить ещё товар",
}
CART_FINISH_BUTTONS = {
    "✅ Buyurtmani yakunlash",
    f"✅ {to_uzbek_cyrillic('Buyurtmani yakunlash')}",
    "✅ Завершить заказ",
}
CONFIRM_ORDER_BUTTONS = {
    "Ha, tasdiqlayman",
    to_uzbek_cyrillic("Ha, tasdiqlayman"),
    "Да, подтверждаю",
}
CANCEL_ORDER_BUTTONS = {
    "Bekor qilish",
    to_uzbek_cyrillic("Bekor qilish"),
    "Отменить",
}


def _uz_text(lang: str, text: str) -> str:
    return to_uzbek_cyrillic(text) if lang == "uz_cyrl" else text

# --- Выбор языка ---
lang_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=label) for label in LANGUAGE_BUTTONS.values()]
    ],
    resize_keyboard=True,
)


# --- Главное меню ---
def get_main_keyboard(lang: str) -> ReplyKeyboardMarkup:
    is_ru = lang == "ru"
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=(
                        "🍗 Интерактивное меню (Сайт)"
                        if is_ru
                        else f"🍗 {_uz_text(lang, 'Interaktiv menyu (Veb-sayt)')}"
                    ),
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ],
            [
                KeyboardButton(
                    text="📦 Сделать заказ"
                    if is_ru
                    else f"📦 {_uz_text(lang, 'Buyurtma berish')}"
                )
            ],
        ],
        resize_keyboard=True,
    )


# Клавиатуры для старых обработчиков (lang == "uz" по умолчанию)
main_btn_uz = get_main_keyboard("uz")
main_btn_ru = get_main_keyboard("ru")


# --- Корзина ---
def get_cart_keyboard(lang: str) -> ReplyKeyboardMarkup:
    is_ru = lang == "ru"
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="➕ Добавить ещё товар"
                    if is_ru
                    else "➕ " + _uz_text(lang, "Yana mahsulot qo'shish")
                )
            ],
            [
                KeyboardButton(
                    text="✅ Завершить заказ"
                    if is_ru
                    else f"✅ {_uz_text(lang, 'Buyurtmani yakunlash')}"
                )
            ],
        ],
        resize_keyboard=True,
    )


cart_btn_uz = get_cart_keyboard("uz")
cart_btn_ru = get_cart_keyboard("ru")


# --- Геолокация ---
def get_location_keyboard(lang: str) -> ReplyKeyboardMarkup:
    is_ru = lang == "ru"
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📍 Отправить геолокацию"
                    if is_ru
                    else f"📍 {_uz_text(lang, 'Geolokatsiyani yuborish')}",
                    request_location=True,
                )
            ]
        ],
        resize_keyboard=True,
    )


location_btn_uz = get_location_keyboard("uz")
location_btn_ru = get_location_keyboard("ru")


# --- Контакт ---
def get_contact_keyboard(lang: str) -> ReplyKeyboardMarkup:
    is_ru = lang == "ru"
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📱 Отправить номер телефона"
                    if is_ru
                    else f"📱 {_uz_text(lang, 'Telefon raqamni yuborish')}",
                    request_contact=True,
                )
            ]
        ],
        resize_keyboard=True,
    )


contact_btn_uz = get_contact_keyboard("uz")
contact_btn_ru = get_contact_keyboard("ru")


# --- Подтверждение заказа ---
def get_confirm_keyboard(lang: str) -> ReplyKeyboardMarkup:
    is_ru = lang == "ru"
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="Да, подтверждаю"
                    if is_ru
                    else _uz_text(lang, "Ha, tasdiqlayman")
                )
            ],
            [
                KeyboardButton(
                    text="Отменить"
                    if is_ru
                    else _uz_text(lang, "Bekor qilish")
                )
            ],
        ],
        resize_keyboard=True,
    )


confirm_btn_uz = get_confirm_keyboard("uz")
confirm_btn_ru = get_confirm_keyboard("ru")
