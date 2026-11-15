"""
Кэш file_id для фотографий товаров.

Telegram отдаёт каждому загруженному/отправленному файлу постоянный file_id.
Если отправлять по file_id, а не по URL — карточка появляется мгновенно,
боту не нужно каждый раз скачивать картинку с сайта.

Схема работы:
1. При старте бот ничего не знает — отправляет по URL (медленно, 1-2 сек).
2. После успешной отправки запоминает file_id (в памяти + в файл).
3. Все последующие отправки — мгновенно по file_id.

Прогреть кэш заранее:  python scripts/warmup_photo_cache.py
"""
import json
import logging
import os
import threading

from aiogram import Bot, types

logger = logging.getLogger(__name__)

CACHE_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bot", "data", "photo_cache.json")

_lock = threading.Lock()
_cache: dict[str, str] = {}
_loaded = False


def _load() -> None:
    global _loaded
    with _lock:
        if _loaded:
            return
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    _cache.update(json.load(f))
                logger.info(f"Кэш фото загружен: {len(_cache)} записей")
            except (json.JSONDecodeError, OSError) as e:
                logger.warning(f"Не удалось прочитать кэш фото: {e}")
        _loaded = True


def _save() -> None:
    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(_cache, f, ensure_ascii=False, indent=1)
    except OSError as e:
        logger.warning(f"Не удалось сохранить кэш фото: {e}")


def get_file_id(url: str) -> str | None:
    """Возвращает кэшированный file_id для URL или None."""
    _load()
    return _cache.get(url)


def cache_file_id(url: str, file_id: str) -> None:
    """Сохраняет file_id для URL (используется ботом и скриптом прогрева)."""
    _load()
    with _lock:
        _cache[url] = file_id
        _save()


async def send_product_photo(bot: Bot, chat_id: int, url: str, caption: str, reply_markup) -> types.Message:
    """Отправляет фото товара: сначала по кэшу file_id, потом по URL.

    При неудаче по file_id — повторяет по URL и обновляет кэш.
    """
    from aiogram.types import InlineKeyboardMarkup

    _load()
    file_id = _cache.get(url)

    if file_id:
        try:
            return await bot.send_photo(
                chat_id=chat_id,
                photo=file_id,
                caption=caption,
                parse_mode="HTML",
                reply_markup=reply_markup,
            )
        except Exception as e:
            logger.warning(f"Отправка по file_id не удалась, пробую по URL: {e}")

    # Отправка по URL
    msg = await bot.send_photo(
        chat_id=chat_id,
        photo=url,
        caption=caption,
        parse_mode="HTML",
        reply_markup=reply_markup,
    )

    # Кэшируем новый file_id
    if msg.photo:
        with _lock:
            _cache[url] = msg.photo[-1].file_id
            _save()

    return msg

