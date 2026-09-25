from aiogram.fsm.context import FSMContext

from bot.services.catalog import format_price


async def get_lang(state: FSMContext) -> str:
    """Достаёт язык из FSM-данных (по умолчанию uz)."""
    data = await state.get_data()
    return data.get("lang", "uz")


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
            prod_name = item.get("name", str(prod_key))
            qty = item.get("quantity", 1)
            price = item.get("price", 0)
        else:
            from bot.services.catalog import get_product

            product = get_product(str(prod_key))
            if product:
                prod_name = product["name"] if lang == "uz" else product.get("name_ru", product["name"])
                price = product["price"]
            else:
                prod_name = str(prod_key).replace("_", " ").capitalize()
                price = 0
            qty = item

        item_sum = price * qty
        total_sum += item_sum

        if lang == "uz":
            products_list += f"• {prod_name}: {qty} dona x {format_price(price)} = {format_price(item_sum)} so'm\n"
        else:
            products_list += f"• {prod_name}: {qty} шт. x {format_price(price)} = {format_price(item_sum)} сум\n"

    return products_list, total_sum
