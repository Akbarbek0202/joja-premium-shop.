"""
Jo'ja — Telegram бот доставки курицы.

Точка входа. Вся логика разложена по пакету bot/:

    bot/config.py            — токен, ID папы, URL веб-приложения
    bot/states.py            — FSM-состояния (заказ + админка)
    bot/locales.py           — тексты на узбекском и русском
    bot/catalog_data.py      — базовый каталог товаров (с фото)
    bot/services/catalog.py  — работа с каталогом + товары из админки
    bot/keyboards/           — reply- и inline-клавиатуры, клавиатуры админки
    bot/handlers/            — обработчики: common, order, admin, notify

Запуск:  python main.py
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from bot.config import TOKEN
from bot.handlers import admin, common, order

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    # Регистрируем обработчики (порядок важен: сначала общие)
    common.register_handlers(dp, bot)
    order.register_handlers(dp, bot)
    admin.register_handlers(dp, bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
