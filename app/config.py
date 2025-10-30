import os

VERSION = "v-0.0.0"

TITLE = f'Ограждение Жалюзи Z110 Аполло    {VERSION}'

# текущий каталог
CWD = os.getcwd()

# каталог статики
STATIC = os.path.join(CWD, 'app', 'static')

# домашняя папка пользователя
HOMEDIR = os.path.expanduser('~')

# файлы
LOG_FILEPATH = os.path.join(CWD, 'logging.log')
ICO_FILEPATH = os.path.join(STATIC, 'ico', 'logo.ico')

# значения для полей формы
WIDTH_MAX_VALUE = 2750
COLOR_TYPES = ('шагрень', 'матовый', 'муар', 'глянец')
HEIGHT_VALUES = [str(count * 110 + 30) for count in range(3, 28)]

# параметры виджетов
TABLE_HEADERS = ("Ширина", "Высота", "RAL", "Структура", "Кол-во")
FORM_MAX_WIDHT = 200
FORM_MIN_WIDTH = 200
TABLE_MIN_WIDTH = 530

FENCE_NAME = 'Секция Z110'
LAMEL_NAME = 'Ламель 124х51'
RAIL_NAME = 'Шина 60х40'
CAP_NAME = 'Крышка 60х40'
SLAT_NAME = 'Планка 40'

FENCE_UNITS = 'шт'
LAMEL_UNITS = 'шт'
RAIL_UNITS = 'пара'
CAP_UNITS = 'шт'
SLAT_UNITS = 'шт'