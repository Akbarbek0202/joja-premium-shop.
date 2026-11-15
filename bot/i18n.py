import re


_UZBEK_CYRILLIC_MAP = {
    "sh": "ш",
    "ch": "ч",
    "ng": "нг",
    "yo": "ё",
    "ya": "я",
    "yu": "ю",
    "ye": "е",
    "o'": "ў",
    "g'": "ғ",
    "a": "а",
    "b": "б",
    "d": "д",
    "e": "е",
    "f": "ф",
    "g": "г",
    "h": "ҳ",
    "i": "и",
    "j": "ж",
    "k": "к",
    "l": "л",
    "m": "м",
    "n": "н",
    "o": "о",
    "p": "п",
    "q": "қ",
    "r": "р",
    "s": "с",
    "t": "т",
    "u": "у",
    "v": "в",
    "x": "х",
    "y": "й",
    "z": "з",
    "w": "в",
    "c": "с",
}
_UZBEK_CYRILLIC_PATTERN = re.compile(
    "|".join(
        re.escape(value)
        for value in sorted(_UZBEK_CYRILLIC_MAP, key=len, reverse=True)
    ),
    re.IGNORECASE,
)


def to_uzbek_cyrillic(text: str) -> str:
    """Transliterates Uzbek Latin text, including the common apostrophe forms."""
    def replace_match(match: re.Match) -> str:
        source = match.group()
        replacement = _UZBEK_CYRILLIC_MAP[source.lower()]
        if source.isupper():
            return replacement.upper()
        if source[0].isupper():
            return replacement.capitalize()
        return replacement

    def transliterate_part(part: str) -> str:
        normalized = re.sub(
            r"(?i)o[ʻ’']",
            lambda match: "Ў" if match.group()[0].isupper() else "ў",
            part,
        )
        normalized = re.sub(
            r"(?i)g[ʻ’']",
            lambda match: "Ғ" if match.group()[0].isupper() else "ғ",
            normalized,
        )
        normalized = normalized.replace("’", "").replace("ʻ", "").replace("'", "")
        return _UZBEK_CYRILLIC_PATTERN.sub(replace_match, normalized)

    return "".join(
        part
        if (
            part.startswith("<") and part.endswith(">")
            or part.startswith("{") and part.endswith("}")
        )
        else transliterate_part(part)
        for part in re.split(r"(<[^>]+>|\{[^{}]+\})", text)
    )


def localized_product_field(product: dict, field: str, lang: str) -> str:
    """Returns a product field in Russian, Uzbek Latin, or Uzbek Cyrillic."""
    if lang == "ru":
        return product.get(f"{field}_ru", product.get(field, ""))
    value = product.get(field, "")
    return to_uzbek_cyrillic(value) if lang == "uz_cyrl" else value


def localized_uzbek_text(text: str, lang: str) -> str:
    return to_uzbek_cyrillic(text) if lang == "uz_cyrl" else text


def _translate_tree_to_uzbek_cyrillic(value):
    if isinstance(value, str):
        return to_uzbek_cyrillic(value)
    if isinstance(value, dict):
        return {key: _translate_tree_to_uzbek_cyrillic(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_translate_tree_to_uzbek_cyrillic(item) for item in value]
    return value
