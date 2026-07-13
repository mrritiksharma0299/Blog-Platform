from django import template

register = template.Library()


@register.filter
def flag_emoji(country):
    """
    Convert country code (IN, JP, US) to 🇮🇳 🇯🇵 🇺🇸
    """
    if not country:
        return ""

    code = str(country.code).upper()

    if len(code) != 2:
        return "🌍"

    return chr(127397 + ord(code[0])) + chr(127397 + ord(code[1]))