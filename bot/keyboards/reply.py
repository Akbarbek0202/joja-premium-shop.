from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

from bot.config import WEBAPP_URL


def get_main_keyboard(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="Интерактивное меню (Сайт)",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ],
            [KeyboardButton(text="Сделать заказ")],
        ],
        resize_keyboard=True,
    )


main_btn_ru = get_main_keyboard()


def get_cart_keyboard(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Добавить ещё товар")],
            [KeyboardButton(text="Завершить заказ")],
        ],
        resize_keyboard=True,
    )


cart_btn_ru = get_cart_keyboard()


def get_location_keyboard(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отправить геолокацию", request_location=True)]
        ],
        resize_keyboard=True,
    )


location_btn_ru = get_location_keyboard()


def get_contact_keyboard(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отправить номер телефона", request_contact=True)]
        ],
        resize_keyboard=True,
    )


contact_btn_ru = get_contact_keyboard()


def get_confirm_keyboard(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Да, подтверждаю")],
            [KeyboardButton(text="Отменить")],
        ],
        resize_keyboard=True,
    )


confirm_btn_ru = get_confirm_keyboard()
