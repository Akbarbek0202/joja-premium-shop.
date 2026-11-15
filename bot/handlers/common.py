import json
import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.handlers import order
from bot.keyboards.reply import get_main_keyboard
from bot.locales import LANGUAGES
from bot.states import OrderState
from bot.services.catalog import get_product
from bot.utils import get_lang
from bot.i18n import localized_product_field

logger = logging.getLogger(__name__)


def register_handlers(dp: Dispatcher, bot: Bot) -> None:
    @dp.message(CommandStart())
    async def start_handler(message: types.Message, state: FSMContext):
        await state.clear()
        await state.update_data(lang="ru")
        await message.answer(LANGUAGES["ru"]["welcome"], reply_markup=get_main_keyboard())

    @dp.message(F.text == "/help")
    async def help_handler(message: types.Message, state: FSMContext):
        lang = await get_lang(state)
        await message.answer(LANGUAGES[lang]["help"], reply_markup=get_main_keyboard(lang))

    @dp.message(F.web_app_data)
    async def web_app_data_handler(message: types.Message, state: FSMContext):
        try:
            data = json.loads(message.web_app_data.data)
        except Exception as e:
            logger.error(f"JSON Error: {e}")
            return

        items = data.get("items", [])

        cart = {}
        for item in items:
            product_id = str(item.get("id", ""))
            product = get_product(product_id) if product_id else None
            prod_name = (
                localized_product_field(product, "name")
                if product
                else localized_product_field(item, "name")
            ) or "Товар"
            qty = int(item.get("quantity", 1))
            price = float(item.get("price", 0))

            cart[prod_name] = {
                "name": prod_name,
                "quantity": qty,
                "price": price,
                "total": qty * price,
            }

        await state.update_data(
            lang="ru",
            cart=dict(cart),
            from_webapp=True,
            total_price=data.get("totalPrice", 0),
        )

        await state.set_state(OrderState.waiting_for_store_name)
        await message.answer(
            LANGUAGES["ru"]["ask_store"],
            reply_markup=types.ReplyKeyboardRemove(),
        )
