import os
import sys
import subprocess

from loguru import logger

from .config import VERSION


def show_file(filepath):
    """ Открывает файл внешней программой """
    if sys.platform == 'win32':
        os.startfile(filepath)
    else:
        subprocess.call(['xdg-open', filepath])


def write_info_to_log(order_info, filepath):
    logger.info('{}: <{}> create order #{} <{}> to {}'.format(
            VERSION, 
            order_info['engineer'],
            order_info['order'], 
            order_info['customer'], 
            filepath,
            )
        )

def shorten_text(text, size=10):
    if len(text) <= size:
        return text
    else:
        return text[:size-3] + '...'
