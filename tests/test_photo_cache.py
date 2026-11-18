import unittest
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from aiogram.exceptions import TelegramAPIError
from PIL import Image

from bot.services import photo_cache


def _webp_image() -> bytes:
    image = Image.new("RGB", (4, 4), "red")
    output = BytesIO()
    image.save(output, format="WEBP")
    return output.getvalue()


class ProductPhotoTests(unittest.IsolatedAsyncioTestCase):
    async def test_local_product_photo_is_read_from_public_folder(self):
        image_data = photo_cache._as_jpeg(_webp_image())
        with TemporaryDirectory() as directory:
            photo_path = Path(directory) / "1.jpg"
            photo_path.write_bytes(image_data)
            with patch.object(photo_cache, "PRODUCT_PHOTO_DIR", directory):
                result = await photo_cache._download_image("/products/1.jpg")

        self.assertEqual(result, image_data)

    async def test_webp_photo_is_uploaded_as_jpeg_and_cached(self):
        image_data = _webp_image()
        sent_message = SimpleNamespace(photo=[SimpleNamespace(file_id="cached-file-id")])
        bot = SimpleNamespace(send_photo=AsyncMock(return_value=sent_message))

        with (
            patch.object(photo_cache, "_loaded", True),
            patch.object(photo_cache, "_cache", {}),
            patch.object(photo_cache, "_download_image", AsyncMock(return_value=image_data)),
            patch.object(photo_cache, "_save"),
        ):
            await photo_cache.send_product_photo(bot, 1, "https://example.test/photo.webp", "Product")

            uploaded_photo = bot.send_photo.await_args.kwargs["photo"]
            with Image.open(BytesIO(uploaded_photo.data)) as result:
                self.assertEqual(result.format, "JPEG")
            self.assertEqual(photo_cache._cache["https://example.test/photo.webp"], "cached-file-id")

    async def test_invalid_cached_file_id_is_replaced(self):
        image_data = _webp_image()
        sent_message = SimpleNamespace(photo=[SimpleNamespace(file_id="replacement-file-id")])
        bot = SimpleNamespace(
            send_photo=AsyncMock(
                side_effect=[
                    TelegramAPIError(method=None, message="invalid file_id"),
                    sent_message,
                ]
            )
        )
        url = "https://example.test/photo.webp"

        with (
            patch.object(photo_cache, "_loaded", True),
            patch.object(photo_cache, "_cache", {url: "invalid-file-id"}),
            patch.object(photo_cache, "_download_image", AsyncMock(return_value=image_data)),
            patch.object(photo_cache, "_save"),
        ):
            await photo_cache.send_product_photo(bot, 1, url, "Product")

            self.assertEqual(bot.send_photo.await_count, 2)
            self.assertEqual(photo_cache._cache[url], "replacement-file-id")

    def test_png_with_transparency_is_convertible(self):
        image = Image.new("RGBA", (2, 2), (255, 0, 0, 0))
        source = BytesIO()
        image.save(source, format="PNG")

        converted = photo_cache._as_jpeg(source.getvalue())

        with Image.open(BytesIO(converted)) as result:
            self.assertEqual(result.format, "JPEG")
            self.assertEqual(result.mode, "RGB")


if __name__ == "__main__":
    unittest.main()
