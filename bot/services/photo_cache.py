"""
Кэш file_id для фотографий товаров.

Telegram отдаёт каждому загруженному/отправленному файлу постоянный file_id.
Если отправлять по file_id, а не по URL — карточка появляется мгновенно,
боту не нужно каждый раз скачивать картинку с сайта.

Схема работы:
1. При первом открытии бот скачивает фото, преобразует его в JPEG и отправляет.
2. После успешной отправки запоминает file_id (в памяти + в файл).
3. Все последующие отправки — мгновенно по file_id.

Прогреть кэш заранее:  python scripts/warmup_photo_cache.py
"""
import json
import logging
import os
import re
import threading
from io import BytesIO

import aiohttp
from aiogram import Bot, types
from aiogram.exceptions import TelegramAPIError
from aiogram.types import BufferedInputFile
from PIL import Image, ImageOps

logger = logging.getLogger(__name__)

CACHE_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bot", "data", "photo_cache.json")
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRODUCT_PHOTO_DIR = os.path.join(PROJECT_ROOT, "public", "products")
MAX_IMAGE_SIZE = 20 * 1024 * 1024

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


async def _download_image(url: str) -> bytes:
    if url.startswith("/products/"):
        filename = url.removeprefix("/products/")
        if not re.fullmatch(r"[A-Za-z0-9_-]+\.jpg", filename):
            raise ValueError("Недопустимый путь к локальному фото товара")
        image_path = os.path.join(PRODUCT_PHOTO_DIR, filename)
        with open(image_path, "rb") as image_file:
            image_data = image_file.read(MAX_IMAGE_SIZE + 1)
        if len(image_data) > MAX_IMAGE_SIZE:
            raise ValueError("Размер фото товара превышает 20 МБ")
        return image_data

    timeout = aiohttp.ClientTimeout(total=20)
    chunks = []
    size = 0

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            async for chunk in response.content.iter_chunked(64 * 1024):
                size += len(chunk)
                if size > MAX_IMAGE_SIZE:
                    raise ValueError("Размер фото товара превышает 20 МБ")
                chunks.append(chunk)

    return b"".join(chunks)


def _as_jpeg(image_data: bytes) -> bytes:
    with Image.open(BytesIO(image_data)) as source:
        image = ImageOps.exif_transpose(source)
        if image.mode in ("RGBA", "LA") or "transparency" in image.info:
            rgba = image.convert("RGBA")
            converted = Image.new("RGB", rgba.size, "white")
            converted.paste(rgba, mask=rgba.getchannel("A"))
        else:
            converted = image.convert("RGB")

        output = BytesIO()
        converted.save(output, format="JPEG", quality=90, optimize=True)
        return output.getvalue()


async def send_product_photo(
    bot: Bot,
    chat_id: int,
    url: str,
    caption: str,
    reply_markup: types.InlineKeyboardMarkup | None = None,
) -> types.Message:
    """Отправляет фото товара: сначала по кэшу file_id, потом после загрузки.

    Фото загружается ботом и преобразуется в JPEG, чтобы Telegram принимал
    изображения в форматах, которые не поддерживаются напрямую.
    """
    _load()
    file_id = get_file_id(url)

    if file_id:
        try:
            return await bot.send_photo(
                chat_id=chat_id,
                photo=file_id,
                caption=caption,
                parse_mode="HTML",
                reply_markup=reply_markup,
            )
        except TelegramAPIError as e:
            logger.warning(f"Отправка по file_id не удалась, загружаю изображение заново: {e}")

    image_data = await _download_image(url)
    msg = await bot.send_photo(
        chat_id=chat_id,
        photo=BufferedInputFile(_as_jpeg(image_data), filename="product.jpg"),
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

