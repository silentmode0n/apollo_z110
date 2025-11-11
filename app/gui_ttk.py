import json

from icecream import ic

from .utils import (
    show_file,
    write_info_to_log,
    validate_value,
)

import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.validation import (
    add_numeric_validation,
    add_option_validation,
    add_range_validation,
    )
from tkinter import filedialog

from .model import Model
from .pdf import PDF
from .config import (
    COLOR_TYPES,
    HEIGHT_VALUES,
    HOMEDIR,
    TABLE_HEADERS,
    TITLE,
    VERSION,
    WIDTH_MAX_VALUE,
    FILETYPES_MAP,
    )


class ProductGroup(ttk.Labelframe):

    def __init__(self, text, bootstyle='dark'):
        super().__init__(text=text, bootstyle=bootstyle)
        self.create_widgets()

    def create_widgets(self):
        table_frame = ttk.Frame(self)
        form_frame = ttk.Frame(self)

        self.table = Tableview(
            table_frame,
            bootstyle='success',
            coldata=TABLE_HEADERS,
            rowdata='',
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

        table_frame.pack(side='left', fill='both', expand=True, anchor='n')
        form_frame.pack(side='left', fill='none', expand=False, anchor='n')

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

    def set_data(self, data):
        self.clear_data()
        if data:
            for product in data.get('products', ''):
                self.add_row_to_table(product.split('_'))

    def set_data_form_json(self, data):
        self.clear_data()
        if data:
            for row in data.get('table', ''):
                self.add_row_to_table(
                    [row['width'], row['height'], row['color'], row['colortype'], row['count']]
                )

    def get_data(self):
        table_data = []
        for row in self.table.get_rows():
            table_row = {}
            table_row['width'] = int(row.values[0]) if row.values[0].isdigit() else ''
            table_row['height'] = int(row.values[1]) if row.values[1].isdigit() else ''
            table_row['color'] = row.values[2]
            table_row['colortype'] = row.values[3]
            table_row['count'] = int(row.values[4]) if row.values[4].isdigit() else ''
            table_data.append(table_row)
        return table_data

    def clear_data(self):
        self.table.delete_rows()


class CommentsGroup(ttk.Labelframe):

    def __init__(self, text, bootstyle='dark'):
        super().__init__(text=text, bootstyle=bootstyle)
        self.create_widgets()

    def create_widgets(self):
        self.comments = ttk.Text(self, height=5)
        self.comments.pack(side='top', fill='x', expand=True, padx=5, pady=5, anchor='n')

    def set_data(self, data):
        self.clear_data()
        if data:
            self.comments.insert('1.0', data.get('comments', ''))

    def get_data(self):
        return self.comments.get('1.0', 'end')

    def clear_data(self):
        self.comments.delete('1.0', 'end')


class OrderGroup(ttk.Labelframe):

    def __init__(self, text, bootstyle='dark'):
        super().__init__(text=text, bootstyle=bootstyle)
        self.create_widgets()

    def create_widgets(self):
        order_group_row1 = ttk.Frame(self)
        order_group_row2 = ttk.Frame(self)

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

        self.customer_entry = ttk.Entry(order_group_row1)
        self.order_entry = ttk.Entry(order_group_row1, width=15)
        self.engineer_entry = ttk.Entry(order_group_row2)
        self.date_entry = ttk.Entry(order_group_row2, width=15)

        customer_label.pack(side='left', fill='y', expand=False,padx=5, anchor='n')
        self.customer_entry.pack(side='left', fill='x', expand=True,padx=5, anchor='n')
        order_label.pack(side='left', fill='y', expand=False,padx=5, anchor='n')
        self.order_entry.pack(side='left', fill='x', expand=False,padx=5, anchor='n')
        engineer_label.pack(side='left', fill='y', expand=False,padx=5, anchor='n')
        self.engineer_entry.pack(side='left', fill='x', expand=True,padx=5, anchor='n')
        date_label.pack(side='left', fill='y', expand=False,padx=5, anchor='n')
        self.date_entry.pack(side='left', fill='x', expand=False,padx=5, anchor='n')

        order_group_row1.pack(side='top', fill='x', expand=True, pady=5, anchor='w')
        order_group_row2.pack(side='top', fill='x', expand=True, pady=5, anchor='e')

    def set_data(self, data):
        self.clear_data()
        if data:
            self.order_entry.insert(0, data.get('order', ''))
            self.customer_entry.insert(0, data.get('customer', ''))
            self.engineer_entry.insert(0, data.get('engineer', ''))

    def get_data(self):
        return {
            'order': self.order_entry.get(),
            'customer': self.customer_entry.get(),
            'engineer': self.engineer_entry.get(),
            'date': self.date_entry.get(),
        }

    def clear_data(self):
        self.order_entry.delete(0, 'end')
        self.customer_entry.delete(0, 'end')
        self.engineer_entry.delete(0, 'end')
        self.date_entry.delete(0, 'end')


class ButtonGroup(ttk.Frame):

    def __init__(self, submit_handler, save_to_handler, load_from_handler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.submit_handler = submit_handler
        self.save_to_handler = save_to_handler
        self.load_from_handler = load_from_handler
        self.create_widgets()

    def create_widgets(self):
        button_submit = ttk.Button(
            self,
            text='Бланк',
            bootstyle='primary',
            command=self.submit_handler)
        button_save_to_json = ttk.Button(
            self,
            text='Сохранить в файл',
            bootstyle='primary-outline',
            command=self.save_to_handler)
        button_load_from_json = ttk.Button(
            self,
            text='Загрузить из файла',
            bootstyle='primary-outline',
            command=self.load_from_handler)

        button_submit.pack(side='left', anchor='w')
        button_load_from_json.pack(side='right', anchor='w')
        button_save_to_json.pack(side='right', anchor='w', padx=5)


class App(ttk.Window):

    def __init__(self):
        super().__init__(title=f'{TITLE}   {VERSION}', themename='cosmo')
        self.debug = False

    def create_widgets(self):
        self.order_group = OrderGroup(text='Информация о заказе')
        self.order_group.pack(side='top', fill='x', expand=False, padx=5, pady=5, anchor='n')
        self.product_group = ProductGroup(text='Информация об изделии')
        self.product_group.pack(side='top', fill='both', expand=True, padx=5, pady=5, anchor='n')
        self.comments_group = CommentsGroup(text='Примечание')
        self.comments_group.pack(side='top', fill='x', expand=False, padx=5, pady=5, anchor='s')
        self.button_group = ButtonGroup(
            submit_handler=self.submit_handler, 
            save_to_handler=self.save_to_json_handler,
            load_from_handler=self.load_from_json_handler,
            )
        self.button_group.pack(side='top', fill='x', expand=False, padx=5, pady=5, anchor='s')

        self.place_window_center()

    def run(self, condition=None, debug=False):
        self.debug = debug
        self.create_widgets()
        if condition:
            self.set_data(condition)
        self.mainloop()

    def get_data(self):
        data = {}
        data['order_info'] = self.order_group.get_data()
        data['comments'] = self.comments_group.get_data()
        data['table'] = self.product_group.get_data()
        return data

    def set_data(self, data):
        self.order_group.set_data(data)
        self.product_group.set_data(data)
        self.comments_group.set_data(data)

    def set_data_form_json(self, data):
        self.order_group.set_data(data.get('order_info'))
        self.comments_group.set_data(data)
        self.product_group.set_data_form_json(data)

    def submit_handler(self):
        """MAIN HANDLER"""
        filepath = self.ask_saveas_filename(self.get_default_filename())
        if filepath:
            data = self.get_data()
            model = Model(data['table'])
            data['fences'] = model.export_fences()
            data['lamels'] = model.export_lamels()
            data['rails'] = model.export_rails()
            data['caps'] = model.export_caps()
            data['slats'] = model.export_slats()

            if self.debug:
                ic(data)

            pdf = PDF(data)
            pdf.create_page()
            pdf.save(filepath)

            write_info_to_log(data['order_info'], filepath)

            show_file(filepath)

    def save_to_json_handler(self):
        filepath = self.ask_saveas_filename(self.get_default_filename(), filetype='json')
        if filepath:
            data = self.get_data()
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file)

    def load_from_json_handler(self):
        filepath = self.ask_open_filename()
        if filepath:
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.set_data_form_json(data)

    def ask_saveas_filename(self, initial_name='result', filetype='pdf'):
        """ return file name """
        filepath = filedialog.asksaveasfilename(
            title='Сохранить как',
            filetypes=FILETYPES_MAP[filetype]['filetypes'],
            initialdir=HOMEDIR,
            initialfile=initial_name,
            defaultextension=FILETYPES_MAP[filetype]['defaultextension']
        )
        return filepath

    def ask_open_filename(self):
        filepath = filedialog.askopenfilename(
            title='Загрузить',
            filetypes=FILETYPES_MAP['json']['filetypes'],
            initialdir=HOMEDIR,
            defaultextension=FILETYPES_MAP['json']['defaultextension'],
        )
        return filepath

    def get_default_filename(self):
        order_info = self.order_group.get_data()
        order = order_info.get('order', 'XXX')
        customer = order_info.get('customer', 'XXXXX')
        return f'{order}-{customer}'
