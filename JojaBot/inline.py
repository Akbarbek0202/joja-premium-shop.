from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from prices import PRODUCT_NAMES


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

WEBAPP_URL = "https://joja-premium-shop-qkbb.vercel.app"


def get_webapp_inline_keyboard(lang: str) -> InlineKeyboardMarkup:
    btn_text = " 🍗 Interaktiv menyu (Veb-sayt)" if lang == "uz" else "🍗 Интерактивное меню (Сайт)"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=btn_text, web_app=WebAppInfo(url=WEBAPP_URL))
            ]
        ]
    )

def get_chicken_keyboard(page: int, lang: str) -> InlineKeyboardMarkup:
    
    prev_text = "⬅️ Ortga" if lang == "uz" else "⬅️ Назад"
    next_text = "Keyingisi ➡️" if lang == "uz" else "Далее ➡️"

    if page == 1:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=PRODUCT_NAMES["golen"][lang], callback_data="cat_golen"), 
                    InlineKeyboardButton(text=PRODUCT_NAMES["file"][lang], callback_data="cat_file")
                ],
                [
                    InlineKeyboardButton(text=PRODUCT_NAMES["maloye_file"][lang], callback_data="cat_maloye_file"), 
                    InlineKeyboardButton(text=PRODUCT_NAMES["bedro"][lang], callback_data="cat_bedro")
                ],
                [
                    InlineKeyboardButton(text=PRODUCT_NAMES["qanot"][lang], callback_data="cat_qanot")
                ],
                [
                    InlineKeyboardButton(text=next_text, callback_data="to_page2")
                ]
            ]
        )
        
    elif page == 2:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=PRODUCT_NAMES["qanot_marinad"][lang], callback_data="cat_qanot_marinad"), 
                    InlineKeyboardButton(text=PRODUCT_NAMES["broyler"][lang], callback_data="cat_broyler")
                ],
                [
                    InlineKeyboardButton(text=PRODUCT_NAMES["okorochka_10kg"][lang], callback_data="cat_okorochka_10kg"), 
                    InlineKeyboardButton(text=PRODUCT_NAMES["golen_10kg"][lang], callback_data="cat_golen_10kg")
                ],
                [
                    InlineKeyboardButton(text=PRODUCT_NAMES["naggets_xrust"][lang], callback_data="cat_naggets_xrust"), 
                    InlineKeyboardButton(text=PRODUCT_NAMES["naggets_sir"][lang], callback_data="cat_naggets_sir")
                ],
                [
                    InlineKeyboardButton(text=PRODUCT_NAMES["naggets_klassik"][lang], callback_data="cat_naggets_klassik"), 
                    InlineKeyboardButton(text=PRODUCT_NAMES["naggets_stripsi"][lang], callback_data="cat_naggets_stripsi")
                ],
                [
                    InlineKeyboardButton(text=PRODUCT_NAMES["naggets_kids"][lang], callback_data="cat_naggets_kids")
                ],
                [
                    InlineKeyboardButton(text=prev_text, callback_data="to_page1"), 
                    InlineKeyboardButton(text=next_text, callback_data="to_page3")
                ]
            ]
        )
        
    elif page == 3:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=PRODUCT_NAMES["golen_lotok"][lang], callback_data="cat_golen_lotok"), 
                    InlineKeyboardButton(text=PRODUCT_NAMES["file_lotok"][lang], callback_data="cat_file_lotok")
                ],
                [
                    InlineKeyboardButton(text=PRODUCT_NAMES["qanot_lotok"][lang], callback_data="cat_qanot_lotok"), 
                    InlineKeyboardButton(text=PRODUCT_NAMES["bedro_lotok"][lang], callback_data="cat_bedro_lotok")
                ],
                [
                    InlineKeyboardButton(text=PRODUCT_NAMES["mfile_lotok"][lang], callback_data="cat_mfile_lotok"), 
                    InlineKeyboardButton(text=PRODUCT_NAMES["jigar_lotok"][lang], callback_data="cat_jigar_lotok")
                ],
                [
                    InlineKeyboardButton(text=PRODUCT_NAMES["yurak_lotok"][lang], callback_data="cat_yurak_lotok"), 
                    InlineKeyboardButton(text=PRODUCT_NAMES["oshqozon_lotok"][lang], callback_data="cat_oshqozon_lotok")
                ],
                [
                    InlineKeyboardButton(text=prev_text, callback_data="to_page2")
                ]
            ]
        )
    



def get_quantity_keyboard(quantity: int, lang: str = "uz") -> InlineKeyboardMarkup:
    btn_confirm_text = "📥 Savatga qo'shish" if lang == "uz" else "📥 Добавить в корзину"
    btn_back_text = "⬅️ Orqaga" if lang == "uz" else "⬅️ Назад"
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➖", callback_data="qty_minus"),
                InlineKeyboardButton(text=f"{quantity} dona" if lang == "uz" else f"{quantity} шт", callback_data="qty_count"),
                InlineKeyboardButton(text="➕", callback_data="qty_plus"),
            ],
            [
                InlineKeyboardButton(text=btn_confirm_text, callback_data="qty_confirm")
            ],
            [
                InlineKeyboardButton(text=btn_back_text, callback_data="qty_back")
            ]
        ]
    )
    return keyboard