import os
import traceback
from icecream import ic

# установка рабочего каталога
os.chdir(os.path.abspath(os.path.dirname(__file__)))

from loguru import logger
from app.gui_ttk import App
from app.parser import parser
from app.config import LOG_FILEPATH
from app.debug import debug_condition

logger.add(LOG_FILEPATH, format="{time} {level} {message}")

if __name__ == "__main__":
    try:
        args = parser.parse_args()
        condition = {
            key: value
            for (key, value) in vars(args).items()
            if value is not None
        }
        if args.debug:
            debug_condition.update(condition)
            condition = debug_condition
            print()
            print("----- Run in DEBUG mode -----")
            print()
            ic(condition)
        app = App()
        app.run(condition)
    except Exception as e:
        logger.critical(f"Критическое исключение!: {e}", exc_info=True)
        ic(traceback.format_exc())
