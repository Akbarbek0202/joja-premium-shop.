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
    total_label = "Jami summa" if lang == "uz" else "Итоговая сумма"
    currency = "so'm" if lang == "uz" else "сум"
    products_list += f"\n💰 <b>{total_label}: {format_price(total_sum)} {currency}</b>"

    order_text = (
        "🔔 <b>Yangi buyurtma keldi!</b>\n\n"
        if lang == "uz"
        else "🔔 <b>Новый заказ!</b>\n\n"
    )
    order_text += (
        f"🏪 <b>Do'kon:</b> {store_name}\n\n" if lang == "uz" else f"🏪 <b>Магазин:</b> {store_name}\n\n"
    )
    order_text += f"📦 <b>Buyurtma tarkibi:</b>\n{products_list}\n" if lang == "uz" else f"📦 <b>Состав заказа:</b>\n{products_list}\n"
    order_text += f"📱 <b>Telefon:</b> {phone}" if lang == "uz" else f"📱 <b>Телефон:</b> {phone}"

    try:
        await bot.send_message(chat_id=PAPA_ID, text=order_text)
        if lat and lon:
            await bot.send_location(chat_id=PAPA_ID, latitude=lat, longitude=lon)
        return True
    except Exception as e:
        logger.error(f"Xatolik: {e}")
        return False
