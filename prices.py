PRODUCT_PRICES = {
    "golen": 42300, 
    "file": 54000, 
    "maloye_file": 49000, 
    "bedro": 40000,
    "qanot_loktevaya": 51000,
    "qanot_plechevaya": 50000,
    "qanot_marinad": 74000, 
    "baffalo": 75000,
    "broyler": 34700, 
    "okorochka_10kg": 315000, 
    "golen_10kg": 372000,
    "naggets_xrust": 36000, 
    "naggets_sir": 36000, 
    "naggets_klassik": 30000, 
    "naggets_stripsi": 47500,
    "naggets_kids": 29000, 
    "kotletalar_burger": 50000,
    "kotletlari_semeyniye": 20000,
    "kotletlari_pishloqli_slivochnie": 28000,
    "golen_lotok": 35000, 
    "file_lotok": 45500, 
    "bedro_lotok": 32000, 
    "mfile_lotok": 40000, 
    "jigar_lotok": 8000, 
    "yurak_lotok": 16000,
    "oshqozon_lotok": 20000
}

PRODUCT_NAMES = {
    "golen": {"uz": "Boldir 🍗", "ru": "Голень 🍗"},
    "file": {"uz": "File 🥩", "ru": "Филе 🥩"},
    "maloye_file": {"uz": "Maloe file 🥩", "ru": "Малое филе 🥩"},
    "bedro": {"uz": "Son 🍖", "ru": "Бедро 🍖"},
    "qanot_loktevaya": {"uz": "Qanot tirsak qismi 🪶", "ru": "Локтевая часть крыла 🪶"},
    "qanot_plechevaya": {"uz": "Qanot yelka qismi 🪶", "ru": "Плечевая часть крыла 🪶"},
    "qanot_marinad": {"uz": "Achchiq qanot 🌶️", "ru": "Крыло в остром маринаде 🌶️"},
    "baffalo": {"uz": "Baffalo 🌶️", "ru": "Баффало 🌶️"},
    "broyler": {"uz": "Broyler 🐓", "ru": "Бройлер 🐓"},
    "okorochka_10kg": {"uz": "Okorochka 10kg 📦", "ru": "Окорочка 10кг 📦"},
    "golen_10kg": {"uz": "Golen 10kg 📦", "ru": "Голень 10кг 📦"},
    "naggets_xrust": {"uz": "Naggetslar Qarsillovchi ✨", "ru": "Наггетсы Хрустящие ✨"},
    "naggets_sir": {"uz": "Naggetslar Pishloqli 🧀", "ru": "Наггетсы Сырные 🧀"},
    "naggets_klassik": {"uz": "Naggetslar Klassik 🍗", "ru": "Наггетсы Классические 🍗"},
    "naggets_stripsi": {"uz": "Naggetslar Stripsi 🥢", "ru": "Стрипсы 🥢"},
    "naggets_kids": {"uz": "Naggetslar Kids 👶", "ru": "Наггетсы Кидс 👶"},
    "kotletalar_burger": {"uz": "Burger uchun kotletalar 🍔", "ru": "Котлеты для бургера 🍔"},
    "kotletlari_semeyniye": {"uz": "Semeyniye kotletlari 🧆", "ru": "Котлеты Семейные 🧆"},
    "kotletlari_pishloqli_slivochnie": {"uz": "Pishloqli va qaymoqli kotletlar 🧀", "ru": "Котлеты Сливочные с сыром 🧀"},
    "golen_lotok": {"uz": "Boldir lotok 📥", "ru": "Голень лоток 📥"},
    "file_lotok": {"uz": "File lotok 📥", "ru": "Филе лоток 📥"},
    "bedro_lotok": {"uz": "Son lotok 📥", "ru": "Бедро лоток 📥"},
    "mfile_lotok": {"uz": "Maloe file lotok 📥", "ru": "Малое филе лоток 📥"},
    "jigar_lotok": {"uz": "Jigar lotok 🩸", "ru": "Печень лоток 🩸"},
    "yurak_lotok": {"uz": "Yurak lotok ❤️", "ru": "Сердце лоток ❤️"},
    "oshqozon_lotok": {"uz": "Oshqozon lotok 📥", "ru": "Желудок лоток 📥"}
}


def format_price(price):
    """Форматирует число в строку с разделением тысяч пробелом (например, 42 300)"""
    return f"{price:,}".replace(",", " ")