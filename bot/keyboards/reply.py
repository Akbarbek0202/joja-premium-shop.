from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

from bot.config import WEBAPP_URL

# --- Выбор языка ---
lang_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="O'zbekcha 🇺🇿"),
            KeyboardButton(text="Русский 🇷🇺"),
        ]
    ],
    resize_keyboard=True,
)


# --- Главное меню ---
def get_main_keyboard(lang: str) -> ReplyKeyboardMarkup:
    is_uz = lang == "uz"
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🍗 Interaktiv menyu (Veb-sayt)" if is_uz else "🍗 Интерактивное меню (Сайт)",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ],
            [
                KeyboardButton(text="📦 Buyurtma berish" if is_uz else "📦 Сделать заказ")
            ],
        ],
        resize_keyboard=True,
    )


# Клавиатуры для старых обработчиков (lang == "uz" по умолчанию)
main_btn_uz = get_main_keyboard("uz")
main_btn_ru = get_main_keyboard("ru")


# --- Корзина ---
def get_cart_keyboard(lang: str) -> ReplyKeyboardMarkup:
    is_uz = lang == "uz"
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Yana mahsulot qo'shish" if is_uz else "➕ Добавить ещё товар")],
            [KeyboardButton(text="✅ Buyurtmani yakunlash" if is_uz else "✅ Завершить заказ")],
        ],
        resize_keyboard=True,
    )


cart_btn_uz = get_cart_keyboard("uz")
cart_btn_ru = get_cart_keyboard("ru")


# --- Геолокация ---
def get_location_keyboard(lang: str) -> ReplyKeyboardMarkup:
    is_uz = lang == "uz"
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📍 Geolokatsiyani yuborish" if is_uz else "📍 Отправить геолокацию",
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
    is_uz = lang == "uz"
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📱 Telefon raqamni yuborish" if is_uz else "📱 Отправить номер телефона",
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
    is_uz = lang == "uz"
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Ha, tasdiqlayman" if is_uz else "Да, подтверждаю")],
            [KeyboardButton(text="Bekor qilish" if is_uz else "Отменить")],
        ],
        resize_keyboard=True,
    )


confirm_btn_uz = get_confirm_keyboard("uz")
confirm_btn_ru = get_confirm_keyboard("ru")
