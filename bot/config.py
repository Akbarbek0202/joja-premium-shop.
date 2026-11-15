import os

from dotenv import load_dotenv

load_dotenv()

# --- Telegram ---
TOKEN = os.getenv("BOT_TOKEN", "")
PAPA_ID = int(os.getenv("PAPA_ID", 0))

# --- Веб-приложение ---
WEBAPP_URL = "https://joja-premium-shop-qkbb.vercel.app"

# --- Файлы данных ---
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bot", "data")
CUSTOM_PRODUCTS_FILE = os.path.join(DATA_DIR, "custom_products.json")
PRODUCT_OVERRIDES_FILE = os.path.join(DATA_DIR, "product_overrides.json")


def ensure_data_dir() -> None:
    """Создаёт папку bot/data, если её нет."""
    os.makedirs(DATA_DIR, exist_ok=True)
