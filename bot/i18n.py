import re
import unicodedata


def strip_emoji(text: str) -> str:
    return "".join(
        character
        for character in text
        if unicodedata.category(character) not in {"So", "Sk", "Me"}
        and ord(character) not in {0x200D, 0xFE0F}
    ).strip()


def localized_product_field(product: dict, field: str, lang: str = "ru") -> str:
    """Returns Russian product text and hides legacy Latin-only Uzbek values."""
    translated = product.get(f"{field}_ru")
    if translated:
        return strip_emoji(translated)

    value = product.get(field, "")
    return strip_emoji(value) if value and not re.search(r"[A-Za-z]", value) else ""
