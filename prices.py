PRODUCT_PRICES = {
    "golen": 42300, 
    "file": 54000, 
    "maloye_file": 49000, 
    "bedro": 40000,
    "qanot": 50000,
    "qanot_marinad": 71500, 
    "broyler": 33500, 
    "okorochka_10kg": 31500, 
    "golen_10kg": 37200,
    "naggets_xrust": 36000, 
    "naggets_sir": 36000, 
    "naggets_klassik": 30000, 
    "naggets_stripsi": 45100,
    "naggets_kids": 29000, 
    "golen_lotok": 35000, 
    "file_lotok": 45500, 
    "qanot_lotok": 42000,
    "bedro_lotok": 32000, 
    "mfile_lotok": 40000, 
    "jigar_lotok": 15000, 
    "yurak_lotok": 18000,
    "oshqozon_lotok": 13000
}

PRODUCT_NAMES = {
    "golen": {"uz": "Boldir 🍗", "ru": "Голень 🍗"},
    "file": {"uz": "File 🥩", "ru": "Филе 🥩"},
    "maloye_file": {"uz": "Maloe file 🥩", "ru": "Малое филе 🥩"},
    "bedro": {"uz": "Son 🍖", "ru": "Бедро 🍖"},
    "qanot": {"uz": "Qanot 🪶", "ru": "Крыло 🪶"},
    "qanot_marinad": {"uz": "Achchiq qanot 🌶️", "ru": "Крыло в остром маринаде 🌶️"},
    "broyler": {"uz": "Broyler 🐓", "ru": "Бройлер 🐓"},
    "okorochka_10kg": {"uz": "Okorochka 10kg 📦", "ru": "Окорочка 10кг 📦"},
    "golen_10kg": {"uz": "Golen 10kg 📦", "ru": "Голень 10кг 📦"},
    "naggets_xrust": {"uz": "Naggetslar Qarsillovchi ✨", "ru": "Наггетсы Хрустящий ✨"},
    "naggets_sir": {"uz": "Naggetslar Pishloqli 🧀", "ru": "Наггетсы Сыр 🧀"},
    "naggets_klassik": {"uz": "Naggetslar Klassik 🍗", "ru": "Наггетсы Классик 🍗"},
    "naggets_stripsi": {"uz": "Naggetslar Stripsi 🥢", "ru": "Стрипсы 🥢"},
    "naggets_kids": {"uz": "Naggetslar Kids 👶", "ru": "Наггетсы Кидс 👶"},
    "golen_lotok": {"uz": "Golen lotok 📥", "ru": "Голень лоток 📥"},
    "file_lotok": {"uz": "File lotok 📥", "ru": "Филе лоток 📥"},
    "qanot_lotok": {"uz": "Qanot lotok 📥", "ru": "Крылышки лоток 📥"},
    "bedro_lotok": {"uz": "Son lotok 📥", "ru": "Бедро лоток 📥"},
    "mfile_lotok": {"uz": "Maloe file lotok 📥", "ru": "Малое филе лоток 📥"},
    "jigar_lotok": {"uz": "Jigar lotok 🩸", "ru": "Печень лоток 🩸"},
    "yurak_lotok": {"uz": "Yurak lotok ❤️", "ru": "Сердечки лоток ❤️"},
    "oshqozon_lotok": {"uz": "Oshqozon lotok 📥", "ru": "Желудки лоток 📥"}
}

def format_price(val: int) -> str:
    return f"{val:,}".replace(",", " ")