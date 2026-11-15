import json
import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.handlers import order
from bot.keyboards.reply import LANGUAGE_BUTTONS, lang_btn, get_main_keyboard
from bot.locales import LANGUAGES
from bot.states import OrderState
from bot.utils import get_lang

logger = logging.getLogger(__name__)


def register_handlers(dp: Dispatcher, bot: Bot) -> None:
    @dp.message(CommandStart())
    async def start_handler(message: types.Message, state: FSMContext):
        await state.clear()
        await state.set_state(OrderState.waiting_for_language)
        await message.answer(
            "Tilni tanlang / Тилни танланг / Выберите язык:",
            reply_markup=lang_btn,
        )

    @dp.message(
        OrderState.waiting_for_language,
        F.text.in_(set(LANGUAGE_BUTTONS.values())),
    )
    async def process_language(message: types.Message, state: FSMContext):
        lang = next(
            language
            for language, label in LANGUAGE_BUTTONS.items()
            if label == message.text
        )
        await state.update_data(lang=lang)
        await message.answer(LANGUAGES[lang]["welcome"], reply_markup=get_main_keyboard(lang))
        await state.set_state(None)

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

        lang = data.get("lang", "uz")
        if not isinstance(lang, str) or lang not in LANGUAGES:
            lang = "uz"
        items = data.get("items", [])

        cart = {}
        for item in items:
            prod_name = item.get("name")
            qty = int(item.get("quantity", 1))
            price = float(item.get("price", 0))

            if prod_name:
                cart[prod_name] = {
                    "name": prod_name,
                    "quantity": qty,
                    "price": price,
                    "total": qty * price,
                }

        await state.update_data(
            lang=lang,
            cart=dict(cart),
            from_webapp=True,
            total_price=data.get("totalPrice", 0),
        )

        await state.set_state(OrderState.waiting_for_store_name)
        await message.answer(
            LANGUAGES[lang]["ask_store"],
            reply_markup=types.ReplyKeyboardRemove(),
        )
