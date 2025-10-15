import argparse


parser = argparse.ArgumentParser(prog='Ограждение Аполло Z110',
                                 description='Генерирует бланк для огражденя Аполло Z110')
parser.add_argument('--debug', action='store_true', help='Режим отладки')
parser.add_argument('--order', help='Номер заказа')
parser.add_argument('--customer', help='Заказчик')
# parser.add_argument('--date', help='Дата готовности')
parser.add_argument('--engineer', help='Инженер')
parser.add_argument('--comments', help='Комментарий')
parser.add_argument('--products', nargs='+', help='Список секций')