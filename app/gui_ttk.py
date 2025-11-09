from icecream import ic

from .utils import (
    show_file,
    write_info_to_log,
    validate_value,
)

from .model import Model
from .pdf import PDF
from .config import (
    COLOR_TYPES,
    HEIGHT_VALUES,
    TABLE_HEADERS,
    TITLE,
    VERSION,
    WIDTH_MAX_VALUE,
    )

import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.validation import (
    add_numeric_validation,
    add_option_validation,
    add_range_validation,
    )


class App(ttk.Window):
    def __init__(self):
        super().__init__(title=f'{TITLE}   {VERSION}', themename='cosmo')
        self.debug = False
        # self.geometry('400x300')

    def create_widgets(self):
        self.get_order_group().pack(side='top', fill='x', expand=False, padx=5, pady=5, anchor='n')
        self.get_product_group().pack(side='top', fill='both', expand=True, padx=5, pady=5, anchor='n')
        self.get_comments_group().pack(side='top', fill='x', expand=False, padx=5, pady=5, anchor='s')
        self.get_button_group().pack(side='top', fill='x', expand=False, padx=5, pady=5, anchor='s')

        self.place_window_center()

    def get_order_group(self):
        order_group = ttk.Labelframe(
            self,
            bootstyle='dark',
            text='Информация о заказе',
            )

        order_group_row1 = ttk.Frame(order_group)
        order_group_row2 = ttk.Frame(order_group)

        order_label = ttk.Label(
            order_group_row1,
            text='Заказ №:',
            width=10,
            )
        customer_label = ttk.Label(
            order_group_row1,
            text='Заказчик:',
            width=10,
            )
        date_label = ttk.Label(
            order_group_row2,
            text='Дата:',
            width=10,
            )
        engineer_label = ttk.Label(
            order_group_row2,
            text='Инженер:',
            width=10,
            )

        customer_entry = ttk.Entry(order_group_row1)
        order_entry = ttk.Entry(order_group_row1, width=15)
        engineer_entry = ttk.Entry(order_group_row2)
        date_entry = ttk.Entry(order_group_row2, width=15)

        customer_label.pack(side='left', fill='y', expand=False,padx=5, anchor='n')
        customer_entry.pack(side='left', fill='x', expand=True,padx=5, anchor='n')
        order_label.pack(side='left', fill='y', expand=False,padx=5, anchor='n')
        order_entry.pack(side='left', fill='x', expand=False,padx=5, anchor='n')
        engineer_label.pack(side='left', fill='y', expand=False,padx=5, anchor='n')
        engineer_entry.pack(side='left', fill='x', expand=True,padx=5, anchor='n')
        date_label.pack(side='left', fill='y', expand=False,padx=5, anchor='n')
        date_entry.pack(side='left', fill='x', expand=False,padx=5, anchor='n')

        order_group_row1.pack(side='top', fill='x', expand=True, pady=5, anchor='w')
        order_group_row2.pack(side='top', fill='x', expand=True, pady=5, anchor='e')

        return order_group

    def get_product_group(self):
        product_group = ttk.Labelframe(
            self,
            bootstyle='dark',
            text='Информация об изделии',
            )
        table_frame = ttk.Frame(product_group)
        form_frame = ttk.Frame(product_group)

        self.table = Tableview(
            table_frame,
            bootstyle='success',
            coldata=TABLE_HEADERS,
            rowdata=['',],
            paginated=False,
            searchable=False,
            yscrollbar=False,
            autofit=True,
            disable_right_click=True,
            )

        for i in range(len(TABLE_HEADERS)):
            self.table.align_heading_center(cid=i)
            self.table.align_column_center(cid=i)

        self.table.pack(side='left', fill='both', expand=True, padx=5, pady=5, anchor='n')

        number_label = ttk.Label(form_frame, text='Кол-во:', width=10)
        self.number_entry = ttk.Entry(form_frame, width=15)
        width_label = ttk.Label(form_frame, text='Ширина:', width=10)
        self.width_entry = ttk.Entry(form_frame, width=15)
        height_label = ttk.Label(form_frame, text='Высота:', width=10)
        self.height_entry = ttk.Combobox(form_frame, width=14, values=HEIGHT_VALUES)
        color_label = ttk.Label(form_frame, text='Цвет:', width=10)
        self.color_entry = ttk.Entry(form_frame, width=15)
        colortype_label = ttk.Label(form_frame, text='Структура:', width=10)
        self.colortype_entry = ttk.Combobox(form_frame, width=14, values=COLOR_TYPES)
        button_add = ttk.Button(form_frame, text='<- Добавить', command=self.button_add_handler)

        number_label.grid(row=0, column=0, padx=5, pady=5)
        self.number_entry.grid(row=0, column=1, padx=5, pady=5)
        width_label.grid(row=1, column=0, padx=5, pady=5)
        self.width_entry.grid(row=1, column=1, padx=5, pady=5)
        height_label.grid(row=2, column=0, padx=5, pady=5)
        self.height_entry.grid(row=2, column=1, padx=5, pady=5)
        color_label.grid(row=3, column=0, padx=5, pady=5)
        self.color_entry.grid(row=3, column=1, padx=5, pady=5)
        colortype_label.grid(row=4, column=0, padx=5, pady=5)
        self.colortype_entry.grid(row=4, column=1, padx=5, pady=5)
        button_add.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        add_numeric_validation(self.number_entry)
        add_range_validation(self.width_entry, 0, WIDTH_MAX_VALUE)
        add_option_validation(self.colortype_entry, COLOR_TYPES)
        add_option_validation(self.height_entry, HEIGHT_VALUES)

        # button_add.bind('<Return>', self.button_add_handler)

        table_frame.pack(side='left', fill='both', expand=True, anchor='n')
        form_frame.pack(side='left', fill='none', expand=None, anchor='n')

        return product_group

    def get_comments_group(self):
        comments_group = ttk.Labelframe(
            self,
            bootstyle='dark',
            text='Примечание',
            )

        self.comments = ttk.Text(
            comments_group,
            height=5,
            )
        self.comments.pack(side='top', fill='x', expand=True, padx=5, pady=5, anchor='n')

        return comments_group

    def get_button_group(self):
        button_group = ttk.Frame(self)
        button_submit = ttk.Button(
            button_group,
            text='Бланк',
            bootstyle='primary',
            )
        button_submit.pack(side='left', anchor='w')

        return button_group

    def validate_form(self):
        number = self.number_entry.get()
        width = self.width_entry.get()
        height = self.height_entry.get()
        color = self.color_entry.get()
        colortype = self.colortype_entry.get()
        if validate_value(number, lambda x: x.isdigit()) and \
            validate_value(width, lambda x: x.isdigit()) and \
            validate_value(width, lambda x: int(x) <= WIDTH_MAX_VALUE) and \
            validate_value(height, lambda x: x in HEIGHT_VALUES) and \
            validate_value(colortype, lambda x: x in COLOR_TYPES):
            return [width, height, color, colortype, number]
        else:
            return False

    def clear_form(self):
        self.number_entry.delete(0, 'end')
        self.width_entry.delete(0, 'end')

    def button_add_handler(self):
        values = self.validate_form()
        if values:
            self.add_row_to_table(values)
            self.clear_form()

    def add_row_to_table(self, values):
        self.table.insert_row(values=values)

    def run(self, condition=None):
        self.create_widgets()
        self.mainloop()
