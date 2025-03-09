import re
from django import template

register = template.Library()

# Map for converting numbers to Unicode superscripts
SUPERSCRIPTS = {
    "0": "⁰",
    "1": "¹",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹"
}

@register.filter
def to_superscript(value):
    """
    Converts exponents in the electronic configuration string to superscripts.
    Exponents are numbers that appear after subshell letters (e.g., 's2', 'p6', 'd10').
    """
    if not value:
        return value

    # Use regex to find patterns like '5f12', '6s2', etc.
    def replace_exponent(match):
        base = match.group(1)  # The letter and any preceding number (e.g., '5f')
        exponent = match.group(2)  # The number to be converted (e.g., '12')
        # Convert each digit in the exponent to superscript
        superscript_exponent = ''.join(SUPERSCRIPTS[digit] for digit in exponent)
        return f"{base}{superscript_exponent}"

    # Regex: Match a letter followed by one or more digits
    pattern = r"([a-zA-Z])(\d+)"
    result = re.sub(pattern, replace_exponent, value)

    return result
