import sys
import os
import json

import asyncio
import logging

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest, TelegramNotFound

from default import (
    lang_btn,
    main_btn_uz, main_btn_ru,
    cart_btn_uz, cart_btn_ru,
    location_btn_uz, location_btn_ru,
    contact_btn_uz, contact_btn_ru,
    confirm_btn_uz, confirm_btn_ru
)
from inline import (
    get_categories_keyboard,
    get_category_products_keyboard,
    get_quantity_keyboard
)
from state import OrderState
from language import LANGUAGES
from prices import PRODUCT_PRICES, PRODUCT_NAMES, format_price

load_dotenv()

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
PAPA_ID = int(os.getenv("PAPA_ID", 0))

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()


async def get_lang(state: FSMContext) -> str:
    data = await state.get_data()
    return data.get("lang", "uz") 


def format_cart_summary(cart: dict, lang: str) -> tuple[str, float]:
    """Универсальная функция для формирования списка товаров и суммы"""
    products_list = ""
    total_sum = 0

    for prod_key, item in cart.items():
        if isinstance(item, dict):
            prod_name = item.get("name", prod_key)
            qty = item.get("quantity", 1)
            price = item.get("price", 0)
        else:
            qty = item
            str_key = str(prod_key)
            
            prod_translations = PRODUCT_NAMES.get(str_key, {})
            prod_name = prod_translations.get(lang, str_key.replace("_", " ").capitalize())
            price = PRODUCT_PRICES.get(str_key, 0)

        item_sum = price * qty
        total_sum += item_sum
        
        if lang == "uz":
            products_list += f"• {prod_name}: {qty} dona x {format_price(price)} = {format_price(item_sum)} so'm\n"
        else:
            products_list += f"• {prod_name}: {qty} шт. x {format_price(price)} = {format_price(item_sum)} сум\n"

    return products_list, total_sum


@dp.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(OrderState.waiting_for_language)
    await message.answer(
        "Assalomu alaykum! Iltimos, tilni tanlang:\n\n"
        "Здравствуйте! Пожалуйста, выберите язык:",
        reply_markup=lang_btn
    )


@dp.message(OrderState.waiting_for_language, F.text.in_({"O'zbekcha 🇺🇿", "Русский 🇷🇺"}))
async def process_language(message: types.Message, state: FSMContext):
    lang = "uz" if "O'zbekcha" in message.text else "ru"
    await state.update_data(lang=lang)

    reply_markup = main_btn_uz if lang == "uz" else main_btn_ru
    await message.answer(
        LANGUAGES[lang]["welcome"], 
        reply_markup=reply_markup
    )
    await state.set_state(None)
        

@dp.message(F.text == "/help")
async def help_handler(message: types.Message, state: FSMContext):
    lang = await get_lang(state)
    markup = main_btn_uz if lang == "uz" else main_btn_ru
    await message.answer(LANGUAGES[lang]["help"], reply_markup=markup)


@dp.message(F.text.in_({"📦 Buyurtma berish", "📦 Сделать заказ"}))
async def start_order(message: types.Message, state: FSMContext):
    lang = await get_lang(state)
    await state.update_data(cart={}, from_webapp=False) 
    await state.set_state(OrderState.waiting_for_store_name)
    await message.answer(
        LANGUAGES[lang]["ask_store"].format(name=""), 
        reply_markup=types.ReplyKeyboardRemove()
    )


@dp.message(OrderState.waiting_for_store_name, F.text)
async def process_store_name(message: types.Message, state: FSMContext):
    lang = await get_lang(state)
    data = await state.get_data()
    await state.update_data(store_name=message.text)
    
    if data.get("from_webapp"):
        markup = location_btn_uz if lang == "uz" else location_btn_ru
        await message.answer(LANGUAGES[lang]["ask_location"], reply_markup=markup)
        await state.set_state(OrderState.waiting_for_address)
    else:
        await state.set_state(OrderState.waiting_for_product)
        keyboard = get_categories_keyboard(lang=lang)
        text = "Kategoriyani tanlang:" if lang == "uz" else "Выберите категорию:"
        await message.answer(text, reply_markup=keyboard)


@dp.message(OrderState.waiting_for_store_name)
async def invalid_store_name(message: types.Message, state: FSMContext):
    lang = await get_lang(state)
    await message.answer(LANGUAGES[lang]["invalid_store"])


# Обработка выбора категории товаров
@dp.callback_query(OrderState.waiting_for_product, F.data.startswith("menu_cat_"))
async def open_category(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(state)
    cat_name = call.data.replace("menu_cat_", "")
    
    text = "Mahsulotni tanlang:" if lang == "uz" else "Выберите товар:"
    keyboard = get_category_products_keyboard(category=cat_name, lang=lang)
    
    try:
        await call.message.edit_text(text, reply_markup=keyboard)
    except (TelegramBadRequest, TelegramNotFound):
        await call.message.answer(text, reply_markup=keyboard)
    await call.answer()


# Возврат к списку категорий
@dp.callback_query(OrderState.waiting_for_product, F.data == "to_categories")
async def back_to_categories(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(state)
    text = "Kategoriyani tanlang:" if lang == "uz" else "Выберите категорию:"
    keyboard = get_categories_keyboard(lang=lang)
    
    try:
        await call.message.edit_text(text, reply_markup=keyboard)
    except (TelegramBadRequest, TelegramNotFound):
        await call.message.answer(text, reply_markup=keyboard)
    await call.answer()


@dp.callback_query(OrderState.waiting_for_product, F.data.startswith("cat_"))
async def select_product(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(state)
    product_key = call.data.replace("cat_", "")
    
    str_key = str(product_key)
    product_translations = PRODUCT_NAMES.get(str_key, {})
    product_name = product_translations.get(lang, str_key.replace("_", " ").capitalize())
    price = PRODUCT_PRICES.get(str_key, 0)
    
    await state.update_data(
        current_product_key=str_key,
        current_product_name=product_name,
        current_qty=1
    )
    
    text = (
        f"Mahsulot: <b>{product_name}</b>\nNarxi: {format_price(price)} so'm\n\nKattaligini/sonini tanlang:" 
        if lang == "uz" else 
        f"Товар: <b>{product_name}</b>\nЦена: {format_price(price)} сум\n\nВыберите количество:"
    )
    
    try:
        await call.message.edit_text(text, reply_markup=get_quantity_keyboard(1, lang))
    except (TelegramBadRequest, TelegramNotFound):
        await call.message.answer(text, reply_markup=get_quantity_keyboard(1, lang))
        
    await state.set_state(OrderState.waiting_for_quantity)
    await call.answer()


@dp.callback_query(OrderState.waiting_for_quantity, F.data.in_({"qty_plus", "qty_minus"}))
async def change_quantity(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(state)
    data = await state.get_data()
    
    current_qty = data.get("current_qty", 1)
    product_name = data.get("current_product_name")
    product_key = str(data.get("current_product_key"))
    price = PRODUCT_PRICES.get(product_key, 0)

    if call.data == "qty_plus":
        current_qty += 1
    elif call.data == "qty_minus" and current_qty > 1:
        current_qty -= 1

    await state.update_data(current_qty=current_qty)

    text = (
        f"Mahsulot: <b>{product_name}</b>\nNarxi: {format_price(price)} so'm\n\nKattaligini/sonini tanlang:" 
        if lang == "uz" else 
        f"Товар: <b>{product_name}</b>\nЦена: {format_price(price)} сум\n\nВыберите количество:"
    )

    try:
        await call.message.edit_text(text, reply_markup=get_quantity_keyboard(current_qty, lang))
    except (TelegramBadRequest, TelegramNotFound):
        pass

    await call.answer()


@dp.callback_query(OrderState.waiting_for_quantity, F.data == "qty_confirm")
async def confirm_quantity(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(state)
    data = await state.get_data()

    current_product_key = str(data.get("current_product_key"))
    current_qty = int(data.get("current_qty", 1))
    
    cart = data.get("cart", {})
    
    if current_product_key in cart:
        if isinstance(cart[current_product_key], dict):
            cart[current_product_key]["quantity"] += current_qty
        else:
            cart[current_product_key] = int(cart[current_product_key]) + current_qty
    else:
        cart[current_product_key] = current_qty

    await state.update_data(cart=cart)

    cart_text = LANGUAGES[lang]["cart_title"]
    products_list, total_sum = format_cart_summary(cart, lang)
    cart_text += products_list

    cart_text += f"\n💰 <b>Jami: {format_price(total_sum)} so'm</b>\n" if lang == "uz" else f"\n💰 <b>Итого: {format_price(total_sum)} сум</b>\n"
    cart_text += LANGUAGES[lang]["cart_footer"]
    markup = cart_btn_uz if lang == "uz" else cart_btn_ru

    try:
        await call.message.delete()
    except (TelegramBadRequest, TelegramNotFound):
        pass

    await call.message.answer(cart_text, reply_markup=markup)
    await state.set_state(OrderState.waiting_for_cart)
    await call.answer()


@dp.callback_query(OrderState.waiting_for_quantity, F.data == "qty_back")
async def back_to_products(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(state)
    await state.set_state(OrderState.waiting_for_product)
    
    keyboard = get_categories_keyboard(lang=lang)
    text = "Kategoriyani tanlang:" if lang == "uz" else "Выберите категорию:"
    try:
        await call.message.edit_text(text, reply_markup=keyboard)
    except (TelegramBadRequest, TelegramNotFound):
        await call.message.answer(text, reply_markup=keyboard)
    await call.answer()


@dp.message(OrderState.waiting_for_cart, F.text.in_({"➕ Yana mahsulot qo'shish", "➕ Добавить ещё товар"}))
async def add_more(message: types.Message, state: FSMContext):
    lang = await get_lang(state)
    await state.set_state(OrderState.waiting_for_product)
    
    keyboard = get_categories_keyboard(lang=lang)
    text = "Kategoriyani tanlang:" if lang == "uz" else "Выберите категорию:"
    await message.answer(text, reply_markup=keyboard)


@dp.message(OrderState.waiting_for_cart, F.text.in_({"✅ Buyurtmani yakunlash", "✅ Завершить заказ"}))
async def finish_order(message: types.Message, state: FSMContext):
    lang = await get_lang(state)
    markup = location_btn_uz if lang == "uz" else location_btn_ru
    await message.answer(LANGUAGES[lang]["ask_location"], reply_markup=markup)
    await state.set_state(OrderState.waiting_for_address)


@dp.message(OrderState.waiting_for_address, F.location)
async def process_location(message: types.Message, state: FSMContext):
    lang = await get_lang(state)
    lat = message.location.latitude
    lon = message.location.longitude
    await state.update_data(lat=lat, lon=lon)
    
    markup = contact_btn_uz if lang == "uz" else contact_btn_ru
    await message.answer(LANGUAGES[lang]["ask_contact"], reply_markup=markup)
    await state.set_state(OrderState.waiting_for_contact)


@dp.message(OrderState.waiting_for_address)
async def invalid_location(message: types.Message, state: FSMContext):
    lang = await get_lang(state)
    markup = location_btn_uz if lang == "uz" else location_btn_ru
    await message.answer(LANGUAGES[lang]["invalid_location"], reply_markup=markup)


@dp.message(OrderState.waiting_for_contact, F.contact)
async def process_contact(message: types.Message, state: FSMContext):
    lang = await get_lang(state)
    phone = message.contact.phone_number
    await state.update_data(contact=phone)
    
    data = await state.get_data()
    store_name = data.get("store_name")
    cart = data.get("cart", {})
    
    products_list, total_sum = format_cart_summary(cart, lang)
    products_list += f"\n💰 <b>Jami summa: {format_price(total_sum)} so'm</b>" if lang == "uz" else f"\n💰 <b>Итоговая сумма: {format_price(total_sum)} сум</b>"
    
    checkout_text = LANGUAGES[lang]["checkout"].format(
        name="",
        store=store_name,
        products=products_list,
        phone=phone
    )
    markup = confirm_btn_uz if lang == "uz" else confirm_btn_ru
    await message.answer(checkout_text, reply_markup=markup)
    await state.set_state(OrderState.waiting_for_confirmation)


@dp.message(OrderState.waiting_for_contact)
async def invalid_contact(message: types.Message, state: FSMContext):
    lang = await get_lang(state)
    markup = contact_btn_uz if lang == "uz" else contact_btn_ru
    await message.answer(LANGUAGES[lang]["invalid_contact"], reply_markup=markup)


@dp.message(OrderState.waiting_for_confirmation, F.text.in_({"Ha, tasdiqlayman", "Да, подтверждаю"}))
async def confirm_order(message: types.Message, state: FSMContext):
    lang = await get_lang(state)
    data = await state.get_data()
    store_name = data.get("store_name")
    cart = data.get("cart", {})
    phone = data.get("contact")
    lat = data.get("lat")
    lon = data.get("lon")

    products_list, total_sum = format_cart_summary(cart, lang)
    products_list += f"\n💰 <b>Jami summa: {format_price(total_sum)} so'm</b>" if lang == "uz" else f"\n💰 <b>Итоговая сумма: {format_price(total_sum)} сум</b>"

    try:
        await bot.send_message(
            chat_id=PAPA_ID,
            text=f"🔔 <b>Yangi buyurtma keldi!</b>\n\n"
                 f"🏪 <b>Do'kon:</b> {store_name}\n\n"
                 f"📦 <b>Buyurtma tarkibi:</b>\n{products_list}\n\n"
                 f"📱 <b>Telefon:</b> {phone}"
        )
        if lat and lon:
            await bot.send_location(chat_id=PAPA_ID, latitude=lat, longitude=lon)
    except Exception as e:
        logging.error(f"Xatolik: {e}")

    markup = main_btn_uz if lang == "uz" else main_btn_ru
    await message.answer(LANGUAGES[lang]["success"], reply_markup=markup)
    await state.clear()


@dp.message(OrderState.waiting_for_confirmation, F.text.in_({"Bekor qilish", "Отменить"}))
async def cancel_order(message: types.Message, state: FSMContext):
    lang = await get_lang(state)
    markup = main_btn_uz if lang == "uz" else main_btn_ru 
    await message.answer(LANGUAGES[lang]["canceled"], reply_markup=markup)
    await state.clear()


@dp.message(F.web_app_data)
async def web_app_data_handler(message: types.Message, state: FSMContext):
    try:
        data = json.loads(message.web_app_data.data)
    except Exception as e:
        logging.error(f"JSON Error: {e}")
        return

    lang = data.get("lang", "uz")
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
                "total": qty * price
            }

    await state.update_data(
        lang=lang, 
        cart=cart, 
        from_webapp=True,
        total_price=data.get("totalPrice", 0)
    )

    await state.set_state(OrderState.waiting_for_store_name)
    await message.answer(
        LANGUAGES[lang]["ask_store"].format(name=""), 
        reply_markup=types.ReplyKeyboardRemove()
    )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())