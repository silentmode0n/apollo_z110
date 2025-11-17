import os

VERSION = "v-1.1"

TITLE = 'Жалюзи Z110'

# текущий каталог
CWD = os.getcwd()

# каталог статики
STATIC = os.path.join(CWD, 'app', 'static')

# домашняя папка пользователя
HOMEDIR = os.path.expanduser('~')

# файлы
LOG_FILEPATH = os.path.join(CWD, 'logging.log')
ICO_FILEPATH = os.path.join(STATIC, 'ico', 'logo.ico')
LOGO_FILEPATH = os.path.join(STATIC, 'logo', 'apollo_logo.png')

# шрифт для PDF
FONT_FILEPATH = os.path.join(STATIC, 'fonts', 'JetBrainsMono-Regular.ttf')
FONT_B_FILEPATH = os.path.join(STATIC, 'fonts', 'JetBrainsMono-Bold.ttf')
FONT_NAME = 'JetBrainsMono'

FILETYPES_MAP = {
    'pdf': {
        'filetypes': (('Document PDF', '*.pdf'), ),
        'defaultextension': '.pdf'
    },
    'json': {
        'filetypes': (('JSON file', '*.json'), ),
        'defaultextension': '.json'
    }
}

WINDOW_THEME = 'cosmo'
LABEL_FRAME_THEME = 'dark'

# значения для полей формы
WIDTH_MAX_VALUE = 3000
COLOR_TYPES = ['шагрень', 'матовый', 'муар', 'глянец']
HEIGHT_VALUES = [str(count * 110 + 30) for count in range(3, 28)]
NAIL_SIZE = '4.0x6'

# параметры виджетов
TABLE_HEADERS = ("Ширина", "Высота", "RAL", "Структура", "Кол-во")

FENCE_TITLE = 'Секции в сборе'
LAMEL_TITLE = 'Ламели 124х51'
RAIL_TITLE = 'Стойки 60х40'
CAP_TITLE = 'Крышки 60х40'
SLAT_TITLE = 'Планки 40'
NAIL_TITLE = 'Крепеж'
COMMENT_TITLE = 'Примечание'