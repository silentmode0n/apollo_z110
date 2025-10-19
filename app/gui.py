from icecream import ic

from .model import Model
from .config import (
    COLOR_TYPES,
    FORM_MAX_WIDHT,
    FORM_MIN_WIDTH,
    TABLE_HEADERS,
    TABLE_MIN_WIDTH,
    TITLE,
    ICO_FILEPATH,
    HOMEDIR,
    WIDTH_MAX_VALUE,
    HEIGHT_MAX_VALUE,
)
from PySide6.QtWidgets import (
    QMainWindow,
    QTableWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QFormLayout,
    QLineEdit,
    QDateEdit,
    QComboBox,
    QTextEdit,
    QPushButton,
    QFileDialog,
    QTableWidgetItem,
)
from PySide6.QtCore import (
    QDate,
    Qt,
)
from PySide6.QtGui import (
    QIntValidator,
    QIcon,
)


class OrderGroup(QGroupBox):
    def __init__(self):
        super().__init__("Информация о заказе")

        self.d_order = QLineEdit()
        self.d_customer = QLineEdit()
        self.d_date = QDateEdit(date=QDate.currentDate())
        self.d_engineer = QLineEdit()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        form_left = QFormLayout()
        col_left = QWidget()
        col_left.setLayout(form_left)
        form_left.addRow("№ Заказа", self.d_order)
        form_left.addRow("Заказчик", self.d_customer)

        form_right = QFormLayout()
        col_right = QWidget()
        col_right.setLayout(form_right)
        form_right.addRow("Дата готовности", self.d_date)
        form_right.addRow("Инженер", self.d_engineer)

        layout.addWidget(col_left)
        layout.addWidget(col_right)

    def get_data(self) -> dict:
        return {
            "order": self.d_order.text(),
            "customer": self.d_customer.text(),
            "date": self.d_date.text(),
            "engineer": self.d_engineer.text(),
        }

    def set_data(self, data: dict):
        for k, v in self.__dict__.items():
            if k.startswith('d_') and k[2:] in data:
                self.__dict__[k].setText(data[k[2:]])


class TableItem(QTableWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.setTextAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )


class ProductGroup(QGroupBox):
    def __init__(self):
        super().__init__("Изделия")

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.table = QTableWidget()
        self.table.setMinimumWidth(TABLE_MIN_WIDTH)
        self.table.setColumnCount(len(TABLE_HEADERS))
        self.table.setHorizontalHeaderLabels(TABLE_HEADERS)
        self.table.cellDoubleClicked.connect(
            lambda: print("clicked")
        )  # TODO: add edit and delete functionals

        form = QWidget()
        form.setMaximumWidth(FORM_MAX_WIDHT)
        form.setMinimumWidth(FORM_MIN_WIDTH)
        form_layout = QFormLayout(form)
        form.setLayout(form_layout)

        self.width_line = QLineEdit(form)
        self.width_line.setValidator(QIntValidator(bottom=0))
        self.width_line.textChanged.connect(
            lambda: self.visual_int_validator(self.width_line, 0, WIDTH_MAX_VALUE)
        )
        self.height_line = QLineEdit(form)
        self.height_line.setValidator(QIntValidator(bottom=0))
        self.height_line.textChanged.connect(
            lambda: self.visual_int_validator(self.height_line, 0, HEIGHT_MAX_VALUE)
        )
        self.color_line = QLineEdit(form)
        self.color_line.setValidator(QIntValidator(bottom=0))
        self.colortype_line = QComboBox(form)
        self.colortype_line.addItems(COLOR_TYPES)
        self.num_line = QLineEdit(form)
        self.num_line.setValidator(QIntValidator(bottom=0))
        self.num_line.textChanged.connect(
            lambda: self.visual_int_validator(self.num_line, 0, 999)
        )
        add_button = QPushButton("Добавить")
        add_button.clicked.connect(self.insert_row_from_button)

        form_layout.addRow(TABLE_HEADERS[0], self.width_line)
        form_layout.addRow(TABLE_HEADERS[1], self.height_line)
        form_layout.addRow(TABLE_HEADERS[2], self.color_line)
        form_layout.addRow(TABLE_HEADERS[3], self.colortype_line)
        form_layout.addRow(TABLE_HEADERS[4], self.num_line)
        form_layout.addRow(add_button)

        layout.addWidget(self.table)
        layout.addWidget(form)

    def visual_int_validator(self, widget, min, max):
        value = widget.text().strip()
        if value.isdigit() and int(value) > min and int(value) <= max:
            widget.setStyleSheet("color: black")
        else:
            widget.setStyleSheet("color: red")

    def get_form_values(self):
        width = self.width_line.text().strip()
        height = self.height_line.text().strip()
        color = self.color_line.text().strip()
        colortype = self.colortype_line.currentText().strip()
        num = self.num_line.text().strip()
        return width, height, color, colortype, num

    def form_is_valid(self):
        width, height, color, colortype, num = self.get_form_values()
        if not width or not height or not color or not num:
            return False
        return True

    def clear_form(self):
        self.width_line.clear()
        self.height_line.clear()
        # self.color_line.clear()
        self.num_line.clear()

    def insert_row_from_button(self):
        if self.form_is_valid():
            self.insert_row(self.get_form_values())
            self.clear_form()

    def insert_row(self, values):
        row = self.table.rowCount()
        self.table.insertRow(row)
        for c, value in enumerate(values):
            self.table.setItem(row, c, TableItem(value))

    def get_data(self) -> dict:
        values = []
        for row in range(self.table.rowCount()):
            row_values = {}
            width = self.table.item(row, 0)
            height = self.table.item(row, 1)
            color = self.table.item(row, 2)
            colortype = self.table.item(row, 3)
            num = self.table.item(row, 4)
            row_values["width"] = int(width.text()) if width else ''
            row_values['height'] = int(height.text()) if height else ''
            row_values['color'] = color.text() if color else ''
            row_values['colortype'] = colortype.text() if colortype else ''
            row_values['num'] = int(num.text()) if num else ''
            values.append(row_values)
        return {'table': values}

    def set_data(self, data: dict): # dict: {products: List["width_height_color_colortype_num"]}
        if 'products' in data:
            for product in data['products']:
                self.insert_row(product.split('_'))


class CommentGroup(QGroupBox):
    def __init__(self):
        super().__init__("Комментарий")

        self.d_comments = QTextEdit()
        # self.d_comments.setMaximumHeight(120) #TODO: set size of comments widget

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        layout.addWidget(self.d_comments)

    def get_data(self) -> dict:
        return {"comments": self.d_comments.toPlainText()}

    def set_data(self, data: dict):
        if 'comments' in data:
            self.d_comments.insertPlainText(data['comments'])


class ButtonGroup(QGroupBox):
    def __init__(self):
        super().__init__("Подготовка чертежа")

        self.submit = QPushButton("Чертеж")

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        layout.addWidget(self.submit)
        layout.addStretch()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle(TITLE)
        icon = QIcon(ICO_FILEPATH)
        self.setWindowIcon(icon)

        main_layout = QVBoxLayout()

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        self.order_group = OrderGroup()
        self.product_group = ProductGroup()
        self.comments_group = CommentGroup()
        self.button_group = ButtonGroup()
        self.button_group.submit.clicked.connect(self.submit_handler)

        main_layout.addWidget(self.order_group)
        main_layout.addWidget(self.product_group)
        main_layout.addWidget(self.comments_group)
        main_layout.addWidget(self.button_group)

    def get_save_as_filename(self) -> str:
        filename, _ = QFileDialog.getSaveFileName(
            caption="Сохранить как", dir=HOMEDIR, filter=("PDF files (*.pdf)")
        )
        return filename

    def get_data(self) -> dict:
        data = {}
        data.update(self.order_group.get_data())
        data.update(self.product_group.get_data())
        data.update(self.comments_group.get_data())
        return data

    def set_data(self, data: dict):
        self.order_group.set_data(data)
        self.comments_group.set_data(data)
        self.product_group.set_data(data)

    def submit_handler(self):
        """MAIN HANDLER"""
        # filepath = self.get_save_as_filename()
        # if filepath:
        #     data = self.get_data()
        #     data['filepath_to_save'] = filepath
        data = self.get_data()
        ic(data)
        model = Model(data)
        ic(model.data)
