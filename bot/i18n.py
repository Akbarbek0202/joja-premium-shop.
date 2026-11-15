import re


def localized_product_field(product: dict, field: str, lang: str = "ru") -> str:
    """Returns Russian product text and hides legacy Latin-only Uzbek values."""
    translated = product.get(f"{field}_ru")
    if translated:
        return translated

    value = product.get(field, "")
    return value if value and not re.search(r"[A-Za-z]", value) else ""
