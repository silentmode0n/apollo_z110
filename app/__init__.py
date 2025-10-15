from PySide6.QtWidgets import QApplication
from .gui import MainWindow


class App(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, condition=None):
        self.window = MainWindow()
        if condition:
            self.window.set_data(condition)
        self.window.show()
        self.exec()