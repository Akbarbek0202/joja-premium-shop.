import logging

from aiogram import Bot

from bot.config import PAPA_ID
from bot.services.catalog import format_price
from bot.utils import format_cart_summary

logger = logging.getLogger(__name__)


async def send_order_notification(bot: Bot, data: dict, lang: str) -> bool:
    """Отправляет заказ папе (текст + геолокация). Возвращает True при успехе."""
    store_name = data.get("store_name")
    cart = data.get("cart", {})
    phone = data.get("contact")
    lat = data.get("lat")
    lon = data.get("lon")

    products_list, total_sum = format_cart_summary(cart, lang)
    products_list += f"\n<b>Итоговая сумма: {format_price(total_sum)} сум</b>"

    order_text = (
        "<b>Новый заказ!</b>\n\n"
        f"<b>Магазин:</b> {store_name}\n\n"
        f"<b>Состав заказа:</b>\n{products_list}\n"
        f"<b>Телефон:</b> {phone}"
    )

    try:
        await bot.send_message(chat_id=PAPA_ID, text=order_text)
        if lat and lon:
            await bot.send_location(chat_id=PAPA_ID, latitude=lat, longitude=lon)
        return True
    except Exception as e:
        logger.error("Не удалось отправить уведомление о заказе: %s", e)
        return False
