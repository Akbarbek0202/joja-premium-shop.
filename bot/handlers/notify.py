import logging

from aiogram import Bot

from bot.config import PAPA_ID
from bot.i18n import localized_uzbek_text
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
    total_label = (
        "Итоговая сумма"
        if lang == "ru"
        else localized_uzbek_text("Jami summa", lang)
    )
    currency = "сум" if lang == "ru" else localized_uzbek_text("so'm", lang)
    products_list += f"\n💰 <b>{total_label}: {format_price(total_sum)} {currency}</b>"

    order_text = (
        "🔔 <b>Новый заказ!</b>\n\n"
        if lang == "ru"
        else f"🔔 <b>{localized_uzbek_text('Yangi buyurtma keldi!', lang)}</b>\n\n"
    )
    store_label = localized_uzbek_text("Do'kon:", lang)
    order_text += (
        f"🏪 <b>Магазин:</b> {store_name}\n\n"
        if lang == "ru"
        else f"🏪 <b>{store_label}</b> {store_name}\n\n"
    )
    order_text += (
        f"📦 <b>Состав заказа:</b>\n{products_list}\n"
        if lang == "ru"
        else f"📦 <b>{localized_uzbek_text('Buyurtma tarkibi:', lang)}</b>\n{products_list}\n"
    )
    order_text += (
        f"📱 <b>Телефон:</b> {phone}"
        if lang == "ru"
        else f"📱 <b>{localized_uzbek_text('Telefon:', lang)}</b> {phone}"
    )

    try:
        await bot.send_message(chat_id=PAPA_ID, text=order_text)
        if lat and lon:
            await bot.send_location(chat_id=PAPA_ID, latitude=lat, longitude=lon)
        return True
    except Exception as e:
        logger.error(f"Xatolik: {e}")
        return False
