from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from prices import PRODUCT_NAMES

WEBAPP_URL = "https://joja-premium-shop-qkbb.vercel.app"

def get_categories_keyboard(lang: str) -> InlineKeyboardMarkup:
    is_uz = (lang == "uz")
    
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🍗 Tovuq qismlari" if is_uz else "🍗 Части курицы", 
                    callback_data="menu_cat_parts"
                ),
                InlineKeyboardButton(
                    text="🌶️ Marinadlar" if is_uz else "🌶️ Маринованное", 
                    callback_data="menu_cat_marinade"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🍟 Naggetslar va Kotletlar" if is_uz else "🍟 Наггетсы и Котлеты", 
                    callback_data="menu_cat_naggets"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📥 Lotoklar" if is_uz else "📥 Лотки", 
                    callback_data="menu_cat_lotok"
                ),
                InlineKeyboardButton(
                    text="🫀 Subproduktlar" if is_uz else "🫀 Субпродукты", 
                    callback_data="menu_cat_sub"
                )
            ]
        ]
    )

def get_category_products_keyboard(category: str, lang: str) -> InlineKeyboardMarkup:
    back_btn = InlineKeyboardButton(
        text="⬅️ Menuga qarash" if lang == "uz" else "⬅️ К категориям", 
        callback_data="to_categories"
    )
    
    buttons = []

    if category == "parts":
        buttons = [
            [
                InlineKeyboardButton(text=PRODUCT_NAMES["golen"][lang], callback_data="cat_golen"),
                InlineKeyboardButton(text=PRODUCT_NAMES["file"][lang], callback_data="cat_file")
            ],
            [
                InlineKeyboardButton(text=PRODUCT_NAMES["maloye_file"][lang], callback_data="cat_maloye_file"),
                InlineKeyboardButton(text=PRODUCT_NAMES["bedro"][lang], callback_data="cat_bedro")
            ],
            [
                InlineKeyboardButton(text=PRODUCT_NAMES["qanot_loktevaya"][lang], callback_data="cat_qanot_loktevaya"),
                InlineKeyboardButton(text=PRODUCT_NAMES["qanot_plechevaya"][lang], callback_data="cat_qanot_plechevaya")
            ],
            [
                InlineKeyboardButton(text=PRODUCT_NAMES["broyler"][lang], callback_data="cat_broyler")
            ],
            [
                InlineKeyboardButton(text=PRODUCT_NAMES["okorochka_10kg"][lang], callback_data="cat_okorochka_10kg"),
                InlineKeyboardButton(text=PRODUCT_NAMES["golen_10kg"][lang], callback_data="cat_golen_10kg")
            ]
        ]

    elif category == "marinade":
        buttons = [
            [
                InlineKeyboardButton(text=PRODUCT_NAMES["qanot_marinad"][lang], callback_data="cat_qanot_marinad")
            ],
            [
                InlineKeyboardButton(text=PRODUCT_NAMES["baffalo"][lang], callback_data="cat_baffalo")
            ]
        ]

    elif category == "naggets":
        buttons = [
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
                InlineKeyboardButton(text=PRODUCT_NAMES["kotletalar_burger"][lang], callback_data="cat_kotletalar_burger"),
                InlineKeyboardButton(text=PRODUCT_NAMES["kotletlari_semeyniye"][lang], callback_data="cat_kotletlari_semeyniye")
            ],
            [
                InlineKeyboardButton(text=PRODUCT_NAMES["kotletlari_pishloqli_slivochnie"][lang], callback_data="cat_kotletlari_pishloqli_slivochnie")
            ]
        ]

    elif category == "lotok":
        buttons = [
            [
                InlineKeyboardButton(text=PRODUCT_NAMES["golen_lotok"][lang], callback_data="cat_golen_lotok"),
                InlineKeyboardButton(text=PRODUCT_NAMES["file_lotok"][lang], callback_data="cat_file_lotok")
            ],
            [
                InlineKeyboardButton(text=PRODUCT_NAMES["bedro_lotok"][lang], callback_data="cat_bedro_lotok"),
                InlineKeyboardButton(text=PRODUCT_NAMES["mfile_lotok"][lang], callback_data="cat_mfile_lotok")
            ]
        ]

    elif category == "sub":
        buttons = [
            [
                InlineKeyboardButton(text=PRODUCT_NAMES["jigar_lotok"][lang], callback_data="cat_jigar_lotok")
            ],
            [
                InlineKeyboardButton(text=PRODUCT_NAMES["yurak_lotok"][lang], callback_data="cat_yurak_lotok"),
                InlineKeyboardButton(text=PRODUCT_NAMES["oshqozon_lotok"][lang], callback_data="cat_oshqozon_lotok")
            ]
        ]

    buttons.append([back_btn])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_quantity_keyboard(quantity: int, lang: str = "uz") -> InlineKeyboardMarkup:
    btn_confirm_text = "📥 Savatga qo'shish" if lang == "uz" else "📥 Добавить в корзину"
    btn_back_text = "⬅️ Orqaga" if lang == "uz" else "⬅️ Назад"
    
    return InlineKeyboardMarkup(
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