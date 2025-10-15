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

# значения для валидатора полей формы
WIDTH_MAX_VALUE = 3000
HEIGHT_MAX_VALUE = 6000

COLOR_TYPES = ('шагрень', 'матовый', 'муар', 'глянец')

# параметры виджетов
TABLE_HEADERS = ("Ширина", "Высота", "RAL", "Структура", "Кол-во")
FORM_MAX_WIDHT = 200
FORM_MIN_WIDTH = 200
TABLE_MIN_WIDTH = 530