import math
import re

def sanitize_reviews(value):
    # None or NaN
    if value is None:
        return None

    if isinstance(value, float):
        if math.isnan(value):
            return None
        return int(value)

    if isinstance(value, int):
        return value

    if isinstance(value, str):
        value = value.strip()

        if value == "":
            return None

        # numeric string
        if value.isdigit():
            return int(value)

        # extract number from text like "120 reviews"
        match = re.search(r"\d+", value)
        if match:
            return int(match.group())

        return None

    return None
