import json

from icecream import ic

from .utils import (
    show_file,
    write_info_to_log,
)

import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.validation import (
    add_numeric_validation,
    add_option_validation,
    add_range_validation,
    )
from tkinter import (
    filedialog,
    messagebox,
    )

from .validators import validate_form
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
    LABEL_FRAME_THEME,
    WINDOW_THEME,
    )


ORDER_GROUP_TITLE = 'Информация о заказе'
PRODUCT_GROUP_TITLE = 'Информация об изделии'
COMMENTS_GROUP_TITLE = 'Примечание'

WIDTH_LABEL = 'Ширина:'
HEIGHT_LABEL = 'Высота:'
COLOR_LABEL = 'Цвет:'
COLORTYPE_LABEL = 'Структура:'
NUMBER_LABEL = 'Кол-во:'


class EditTableRowModal(ttk.Toplevel):
    def __init__(self, title, table_row):
        super().__init__(title)
        self._table_row = table_row
        self.create_widgets()
        self.place_window_center()

    def create_widgets(self):
        ttk.Label(self, text=WIDTH_LABEL, width=10).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        ttk.Label(self, text=HEIGHT_LABEL, width=10).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        ttk.Label(self, text=COLOR_LABEL, width=10).grid(row=2, column=0, padx=5, pady=5, sticky='w')
        ttk.Label(self, text=COLORTYPE_LABEL, width=10).grid(row=3, column=0, padx=5, pady=5, sticky='w')
        ttk.Label(self, text=NUMBER_LABEL, width=10).grid(row=4, column=0, padx=5, pady=5, sticky='w')

        self.width_entry = ttk.Entry(self, width=15)
        self.height_entry = ttk.Combobox(self, width=14, values=HEIGHT_VALUES)
        self.color_entry = ttk.Entry(self, width=15)
        self.number_entry = ttk.Entry(self, width=15)
        self.colortype_entry = ttk.Combobox(self, width=14, values=COLOR_TYPES)

        self.width_entry.grid(row=0, column=1, padx=5, pady=5, sticky='nswe')
        self.height_entry.grid(row=1, column=1, padx=5, pady=5, sticky='nswe')
        self.color_entry.grid(row=2, column=1, padx=5, pady=5, sticky='nswe')
        self.colortype_entry.grid(row=3, column=1, padx=5, pady=5, sticky='nswe')
        self.number_entry.grid(row=4, column=1, padx=5, pady=5, sticky='nswe')

        self.width_entry.insert(0, self._table_row.values[0])
        self.height_entry.insert(0, self._table_row.values[1])
        self.color_entry.insert(0, self._table_row.values[2])
        self.colortype_entry.insert(0, self._table_row.values[3])
        self.number_entry.insert(0, self._table_row.values[4])

        button_frame = ttk.Frame(self)
        button_frame.grid(row=5, columnspan=2, padx=5, pady=5)

        ttk.Button(
            button_frame, text='Сохранить', bootstyle='primary', command=self.save
            ).pack(side='left')
        ttk.Button(
            button_frame, text='Удалить', bootstyle='danger-outline', command=self.delete
            ).pack(side='left', padx=5)
        ttk.Button(
            button_frame, text='Отмена', bootstyle='primary-outline', command=self.cancel
            ).pack(side='left')

        add_numeric_validation(self.number_entry)
        add_range_validation(self.width_entry, 0, WIDTH_MAX_VALUE)
        add_option_validation(self.colortype_entry, COLOR_TYPES)
        add_option_validation(self.height_entry, HEIGHT_VALUES)

    def save(self):
        number = self.number_entry.get()
        width = self.width_entry.get()
        height = self.height_entry.get()
        color = self.color_entry.get()
        colortype = self.colortype_entry.get()

        if validate_form(width, height, color, colortype, number):
            self._table_row.values = [width, height, color, colortype, number]
            self._table_row.refresh()
            self.destroy()

    def delete(self):
        self._table_row.delete()
        self.destroy()

    def cancel(self):
        self.destroy()


class ProductGroup(ttk.Labelframe):

    def __init__(self,master, text):
        super().__init__(master=master, text=text, bootstyle=LABEL_FRAME_THEME)
        self.create_widgets()

    def create_widgets(self):
        table_frame = ttk.Frame(self)
        form_frame = ttk.Frame(self)

        self.table = self.create_table(table_frame, self.table_handler)
        self.table.pack(side='top', fill='both', expand=True, padx=5, pady=5, anchor='n')

        ttk.Label(table_frame, text='* Двойной клик по строке для редактироания', bootstyle='secondary').pack(
            side='top', fill='x', expand=False, padx=5, pady=5, anchor='s'
            )

        number_label = ttk.Label(form_frame, text=NUMBER_LABEL, width=10)
        self.number_entry = ttk.Entry(form_frame, width=15)
        width_label = ttk.Label(form_frame, text=WIDTH_LABEL, width=10)
        self.width_entry = ttk.Entry(form_frame, width=15)
        height_label = ttk.Label(form_frame, text=HEIGHT_LABEL, width=10)
        self.height_entry = ttk.Combobox(form_frame, width=12, values=HEIGHT_VALUES)
        color_label = ttk.Label(form_frame, text=COLOR_LABEL, width=10)
        self.color_entry = ttk.Entry(form_frame, width=15)
        colortype_label = ttk.Label(form_frame, text=COLORTYPE_LABEL, width=10)
        self.colortype_entry = ttk.Combobox(form_frame, width=12, values=COLOR_TYPES)
        button_add = ttk.Button(form_frame, text='Добавить', command=self.button_add_handler)

        width_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.width_entry.grid(row=0, column=1, padx=5, pady=5, sticky='nswe')
        height_label.grid(row=1, column=0, padx=5, pady=0, sticky='w')
        self.height_entry.grid(row=1, column=1, padx=5, pady=0, sticky='nswe')
        number_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.number_entry.grid(row=2, column=1, padx=5, pady=5, sticky='nswe')
        color_label.grid(row=3, column=0, padx=5, pady=0, sticky='w')
        self.color_entry.grid(row=3, column=1, padx=5, pady=0, sticky='nswe')
        colortype_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.colortype_entry.grid(row=4, column=1, padx=5, pady=5, sticky='nswe')
        button_add.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        add_numeric_validation(self.number_entry)
        add_range_validation(self.width_entry, 0, WIDTH_MAX_VALUE)
        add_option_validation(self.colortype_entry, COLOR_TYPES)
        add_option_validation(self.height_entry, HEIGHT_VALUES)

        table_frame.pack(side='left', fill='both', expand=True, anchor='n')
        form_frame.pack(side='left', fill='none', expand=False, anchor='n')

    def create_table(self, parent, handler):
        table = Tableview(
            parent,
            bootstyle='success',
            coldata=TABLE_HEADERS,
            rowdata='',
            paginated=False,
            searchable=False,
            yscrollbar=False,
            autofit=True,
            disable_right_click=True,
            )
        table.configure(selectmode='browse')
        table.view.bind('<Double-1>', handler)

        for i in range(len(TABLE_HEADERS)):
            table.align_heading_center(cid=i)
            table.align_column_center(cid=i)

        return table

    def clear_form(self):
        self.number_entry.delete(0, 'end')
        self.width_entry.delete(0, 'end')

    def button_add_handler(self):
        number = self.number_entry.get()
        width = self.width_entry.get()
        height = self.height_entry.get()
        color = self.color_entry.get()
        colortype = self.colortype_entry.get()

        if validate_form(width, height, color, colortype, number):
            self.add_row_to_table([width, height, color, colortype, number])
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
            table_row['width'] = row.values[0]
            table_row['height'] = row.values[1]
            table_row['color'] = row.values[2]
            table_row['colortype'] = row.values[3]
            table_row['count'] = row.values[4]
            table_data.append(table_row)
        return table_data

    def clear_data(self):
        self.table.delete_rows()

    def table_handler(self, event):
        tablerow = self.get_selected_tablerow()
        if tablerow:
            dialog = EditTableRowModal('Редактировать данные', tablerow)
            self.master.wait_window(dialog)

    def get_selected_tablerow(self):
        selected = self.table.view.selection()
        if selected:
            return self.table.iidmap.get(selected[0])

    def del_selected_tablerow(self):
        tablerow = self.get_selected_tablerow()
        if tablerow:
            tablerow.delete()



class CommentsGroup(ttk.Labelframe):

    def __init__(self, master, text):
        super().__init__(master=master, text=text, bootstyle=LABEL_FRAME_THEME)
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

    def __init__(self, master, text):
        super().__init__(master=master, text=text, bootstyle=LABEL_FRAME_THEME)
        self.create_widgets()

    def create_widgets(self):
        order_group_col1 = ttk.Frame(self)
        order_group_col1.columnconfigure(1, weight=1)
        order_group_col2 = ttk.Frame(self)

        order_label = ttk.Label(
            order_group_col2,
            text='Заказ №:',
            width=10,
            )
        customer_label = ttk.Label(
            order_group_col1,
            text='Заказчик:',
            width=10,
            )
        date_label = ttk.Label(
            order_group_col2,
            text='Дата:',
            width=10,
            )
        engineer_label = ttk.Label(
            order_group_col1,
            text='Инженер:',
            width=10,
            )

        self.customer_entry = ttk.Entry(order_group_col1, width=15)
        self.order_entry = ttk.Entry(order_group_col2, width=15)
        self.engineer_entry = ttk.Entry(order_group_col1)
        self.date_entry = ttk.DateEntry(
            order_group_col2, 
            firstweekday=0, 
            popup_title='Календарь',
            width=10,
            )

        customer_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.customer_entry.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        engineer_label.grid(row=1, column=0, padx=5, pady=0, sticky='w')
        self.engineer_entry.grid(row=1, column=1, padx=5, pady=0, sticky='nsew')
        order_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.order_entry.grid(row=0, column=1, padx=5, pady=5, sticky='e')
        date_label.grid(row=1, column=0, padx=5, pady=0, sticky='e')
        self.date_entry.grid(row=1, column=1, padx=5, pady=0, sticky='nsew')

        order_group_col1.pack(side='left', fill='both', expand=True, pady=5, anchor='n')
        order_group_col2.pack(side='left', fill='none', expand=False, pady=5, anchor='n')

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
            'date': self.date_entry.entry.get(),
        }

    def clear_data(self):
        self.order_entry.delete(0, 'end')
        self.customer_entry.delete(0, 'end')
        self.engineer_entry.delete(0, 'end')
        self.date_entry.entry.delete(0, 'end')


class ButtonGroup(ttk.Frame):

    def __init__(self, master, submit_handler, save_to_handler, load_from_handler, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
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
        super().__init__(title=f'{TITLE}   {VERSION}', themename=WINDOW_THEME)
        self.debug = False

    def create_widgets(self):
        self.order_group = OrderGroup(self, text=ORDER_GROUP_TITLE)
        self.order_group.pack(side='top', fill='x', expand=False, padx=5, pady=5, anchor='n')
        self.product_group = ProductGroup(self, text=PRODUCT_GROUP_TITLE)
        self.product_group.pack(side='top', fill='both', expand=True, padx=5, pady=5, anchor='n')
        self.comments_group = CommentsGroup(self, text=COMMENTS_GROUP_TITLE)
        self.comments_group.pack(side='top', fill='x', expand=False, padx=5, pady=5, anchor='s')
        self.button_group = ButtonGroup(
            self,
            submit_handler=self.submit_handler, 
            save_to_handler=self.save_to_json_handler,
            load_from_handler=self.load_from_json_handler,
            )
        self.button_group.pack(side='top', fill='x', expand=False, padx=5, pady=5, anchor='s')

        self.resizable(width=False, height=True)
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
            try:
                model = Model(data['table'])
                data['fences'] = model.export_fences()
                data['lamels'] = model.export_lamels()
                data['rails'] = model.export_rails()
                data['caps'] = model.export_caps()
                data['slats'] = model.export_slats()
                data['nails'] = model.export_nails()
            except ValueError:
                messagebox.showwarning('Ошибка!', 'Ошибка данных таблицы.')
                return None

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
