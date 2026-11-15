from aiogram.fsm.context import FSMContext

from bot.i18n import localized_product_field
from bot.services.catalog import format_price


async def get_lang(state: FSMContext) -> str:
    """Возвращает единственный поддерживаемый язык бота."""
    return "ru"


def format_cart_summary(cart: dict, lang: str) -> tuple[str, float]:
    """Формирует список товаров и общую сумму заказа.

    Поддерживает два формата корзины:
    - из обычного бота: {product_id: quantity}
    - из веб-приложения: {name: {"name":..., "quantity":..., "price":...}}
    """
    products_list = ""
    total_sum = 0

    for prod_key, item in cart.items():
        if isinstance(item, dict):
            prod_name = localized_product_field(item, "name") or "Товар"
            qty = item.get("quantity", 1)
            price = item.get("price", 0)
        else:
            from bot.services.catalog import get_product

            product = get_product(str(prod_key))
            if product:
                prod_name = localized_product_field(product, "name") or "Товар"
                price = product["price"]
            else:
                prod_name = "Товар"
                price = 0
            qty = item

        item_sum = price * qty
        total_sum += item_sum

        products_list += f"• {prod_name}: {qty} шт. x {format_price(price)} = {format_price(item_sum)} сум\n"

    return products_list, total_sum
