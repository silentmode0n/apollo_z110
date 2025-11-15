from .config import (
	WIDTH_MAX_VALUE,
	HEIGHT_VALUES,
	COLOR_TYPES,
	)


def validate_form(width, height, color, colortype, number):
        if number.isdigit() and \
            width.isdigit() and \
            int(width) <= WIDTH_MAX_VALUE and \
            height in HEIGHT_VALUES and \
            colortype in COLOR_TYPES:
            
            return True
        else:
            return False
