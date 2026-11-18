"""
Прогрев кэша фото: бот заранее отправляет каждую картинку и сохраняет file_id.
После этого карточки товаров открываются мгновенно.

Запуск (один раз после смены картинок или на новом сервере):
    python scripts/warmup_photo_cache.py
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aiogram import Bot  # noqa: E402

from bot.catalog_data import BASE_PRODUCTS  # noqa: E402
from bot.config import TOKEN, PAPA_ID  # noqa: E402
from bot.services.photo_cache import get_file_id, send_product_photo  # noqa: E402


async def warmup() -> None:
    if not TOKEN:
        print("❌ BOT_TOKEN не найден в .env")
        return

    if not PAPA_ID:
        print("❌ PAPA_ID не найден в .env — прогреву некуда отправлять фото.")
        print("   Укажи PAPA_ID в .env и запусти снова.")
        return

    bot = Bot(token=TOKEN)
    me = await bot.get_me()
    print(f"🤖 Бот: @{me.username}")
    print(f"🔥 Прогреваю кэш для {len(BASE_PRODUCTS)} товаров...\n")

    ok = 0
    skipped = 0
    failed = 0

    for p in BASE_PRODUCTS:
        url = p.get("image", "")
        name = p["name"]
        if not url:
            print(f"⏭  {name}: нет фото")
            skipped += 1
            continue

        if get_file_id(url):
            print(f"✓  {name}: уже в кэше")
            ok += 1
            continue

        try:
            # Telegram отдаёт file_id только после реальной отправки.
            await send_product_photo(bot, PAPA_ID, url, name)
            ok += 1
            print(f"✓  {name}: закэшировано")
        except Exception as e:
            failed += 1
            print(f"✗  {name}: {type(e).__name__}: {str(e)[:60]}")

    print(f"\n📊 Готово: {ok} ок, {skipped} без фото, {failed} ошибок")
    print("Теперь карточки товаров открываются мгновенно ⚡")

    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(warmup())
