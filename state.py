from aiogram.fsm.state import State, StatesGroup

class OrderState(StatesGroup):
    waiting_for_language = State()       
    waiting_for_store_name = State()
    waiting_for_product = State()
    waiting_for_quantity = State()
    waiting_for_cart = State()
    waiting_for_address = State()
    waiting_for_contact = State()
    waiting_for_confirmation = State()