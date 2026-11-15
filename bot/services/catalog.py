"""
Сервис каталога товаров.

Все товары хранятся в двух местах:
1. BASE_PRODUCTS (bot/catalog_data.py) — товары, зашитые в код.
2. bot/data/custom_products.json — товары, добавленные папой через админку.
3. bot/data/product_overrides.json — изменения базовых товаров.
"""
import json
import logging
import os

from bot.config import CUSTOM_PRODUCTS_FILE, PRODUCT_OVERRIDES_FILE, ensure_data_dir
from bot.catalog_data import BASE_PRODUCTS

logger = logging.getLogger(__name__)

# --- Категории ---
CATEGORIES = ["parts", "marinade", "naggets", "lotok", "sub"]


def _load_custom_products() -> list:
    """Загружает товары, добавленные через админку."""
    if not os.path.exists(CUSTOM_PRODUCTS_FILE):
        return []
    try:
        with open(CUSTOM_PRODUCTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"Не удалось прочитать {CUSTOM_PRODUCTS_FILE}: {e}")
        return []


def _save_custom_products(products: list) -> None:
    """Сохраняет товары, добавленные через админку."""
    ensure_data_dir()
    with open(CUSTOM_PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)


def _load_product_overrides() -> dict:
    """Загружает изменения базовых товаров."""
    if not os.path.exists(PRODUCT_OVERRIDES_FILE):
        return {}
    try:
        with open(PRODUCT_OVERRIDES_FILE, "r", encoding="utf-8") as f:
            overrides = json.load(f)
        return overrides if isinstance(overrides, dict) else {}
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"Не удалось прочитать {PRODUCT_OVERRIDES_FILE}: {e}")
        return {}


def _save_product_overrides(overrides: dict) -> None:
    ensure_data_dir()
    with open(PRODUCT_OVERRIDES_FILE, "w", encoding="utf-8") as f:
        json.dump(overrides, f, ensure_ascii=False, indent=2)


def get_all_products() -> list:
    """Все товары: базовые + добавленные папой."""
    overrides = _load_product_overrides()
    base_products = [
        {**product, **overrides.get(str(product["id"]), {})}
        for product in BASE_PRODUCTS
    ]
    return base_products + _load_custom_products()


def get_products_by_category(category: str) -> list:
    """Товары конкретной категории."""
    return [p for p in get_all_products() if p.get("category") == category]


def get_product(product_id: str) -> dict | None:
    """Находит товар по id."""
    for p in get_all_products():
        if str(p["id"]) == str(product_id):
            return p
    return None


def add_product(name: str, price: int, description: str, image: str, category: str) -> dict:
    """Добавляет новый товар (через админку) и возвращает его."""
    products = _load_custom_products()

    # Генерируем уникальный id: max существующего числового id + 1
    all_ids = []
    for p in get_all_products():
        try:
            all_ids.append(int(p["id"]))
        except (ValueError, TypeError):
            pass
    new_id = str(max(all_ids, default=0) + 1)

    product = {
        "id": new_id,
        "name": name,
        "name_ru": name,
        "category": category,
        "price": price,
        "description": description,
        "description_ru": description,
        "image": image or "",
    }
    products.append(product)
    _save_custom_products(products)
    logger.info(f"Добавлен товар: {product}")
    return product


def delete_product(product_id: str) -> dict | None:
    """Удаляет товар, добавленный через админку. Возвращает удалённый товар или None."""
    products = _load_custom_products()
    for i, p in enumerate(products):
        if str(p["id"]) == str(product_id):
            removed = products.pop(i)
            _save_custom_products(products)
            logger.info(f"Удалён товар: {removed}")
            return removed
    return None


def update_product(product_id: str, changes: dict) -> dict | None:
    """Обновляет товар и возвращает его; базовые товары сохраняются как переопределения."""
    allowed_fields = {
        "name",
        "name_ru",
        "price",
        "description",
        "description_ru",
        "image",
        "category",
    }
    if not changes or not set(changes).issubset(allowed_fields):
        raise ValueError("Недопустимые поля товара")
    if "category" in changes and changes["category"] not in CATEGORIES:
        raise ValueError("Недопустимая категория")

    products = _load_custom_products()
    for product in products:
        if str(product["id"]) == str(product_id):
            product.update(changes)
            _save_custom_products(products)
            logger.info(f"Изменён товар: {product}")
            return product

    base_product = next(
        (product for product in BASE_PRODUCTS if str(product["id"]) == str(product_id)),
        None,
    )
    if base_product is None:
        return None

    overrides = _load_product_overrides()
    overrides.setdefault(str(product_id), {}).update(changes)
    _save_product_overrides(overrides)
    updated = {**base_product, **overrides[str(product_id)]}
    logger.info(f"Изменён базовый товар: {updated}")
    return updated


def format_price(price) -> str:
    """Форматирует число в строку с разделением тысяч пробелом (например, 42 300)."""
    try:
        price = int(float(price))
    except (ValueError, TypeError):
        price = 0
    return f"{price:,}".replace(",", " ")
