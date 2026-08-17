from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

WEBAPP_URL = "https://joja-premium-shop-qkbb.vercel.app"

lang_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="O'zbekcha 🇺🇿"),
            KeyboardButton(text="Русский 🇷🇺")
        ]
    ],
    resize_keyboard=True
)

main_btn_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍗 Interaktiv menyu (Veb-sayt)", web_app=WebAppInfo(url=WEBAPP_URL))],
        [KeyboardButton(text="📦 Buyurtma berish")]
    ],
    resize_keyboard=True
)

main_btn_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍗 Интерактивное меню (Сайт)", web_app=WebAppInfo(url=WEBAPP_URL))],
        [KeyboardButton(text="📦 Сделать заказ")]
    ],
    resize_keyboard=True
)

cart_btn_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Yana mahsulot qo'shish")],
        [KeyboardButton(text="✅ Buyurtmani yakunlash")]
    ],
    resize_keyboard=True
)

location_btn_uz = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📍 Geolokatsiyani yuborish", request_location=True)]],
    resize_keyboard=True
)

contact_btn_uz = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]],
    resize_keyboard=True
)

confirm_btn_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Ha, tasdiqlayman")],
        [KeyboardButton(text="Bekor qilish")]
    ],
    resize_keyboard=True
)

cart_btn_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Добавить ещё товар")],
        [KeyboardButton(text="✅ Завершить заказ")]
    ],
    resize_keyboard=True
)

location_btn_ru = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📍 Отправить геолокацию", request_location=True)]],
    resize_keyboard=True
)

contact_btn_ru = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)]],
    resize_keyboard=True
)

confirm_btn_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да, подтверждаю")],
        [KeyboardButton(text="Отменить")]
    ],
    resize_keyboard=True
)