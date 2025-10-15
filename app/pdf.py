from fpdf import FPDF


BLACK = (0, 0, 0)
RED = (250, 0, 0)

#TODO: move templates in individual module
INFO_FRAME_FOR_MAF = """Размер:             {width} х {height} мм
Рама:               {bridge}
Просвет:            {cliarance} мм
Фрамуга:            {bridge_height} мм"""

INFO_FRAME_FOR_CL = """Ширина:             {width} мм
Высота:             {height} мм
Рама:               {bridge}
Просвет:            {cliarance} мм
Фрамуга:            {bridge_height} мм
Вид заполнения:     {fill}"""

INFO_DOOR = """Размер:             {door_width} х {door_height} мм
Открытие:           {open}
Петли (со двора):   {side}"""

INFO_FILL = """Вид заполнения:     {fill}
Размер на створку:  {door_fill_width} х {door_fill_height} мм
Размер на фрамугу:  {bridge_fill_width} х {bridge_fill_height} мм"""

INFO_COLOR = """Цвет рамы:          {frame_color} {frame_color_name} {color_type}
Заполнение снаружи: {fill_color_out} {fill_color_out_name}
Заполнение изнутри: {fill_color_in} {fill_color_in_name}"""

INFO_OPEN = """Направление:        {open}
Петли (со двора):   {side}"""

INFO_OPTIONS = """Замок:              {lock}
Ручка снаружи:      {handle_out}
Ручка изнутри:      {handle_in}
Гибкий переход:     {flexible_tube}
Доводчик:           {auto_closer}
Нащельник:          {batten} {batten_lenght} мм {batten_num} шт
Стикер Аполло:      {sticker}"""

#TODO: edit PDFCreator class
class PDFCreator(FPDF):
    """ """ 
    def __init__(self, config, data):
        super().__init__('L', 'mm', 'A4')
        self.data = data
        self.ver = config['version']
        self.font_size_main = config['font_size_main']
        self.font_size_header = config['font_size_header']
        self.logo_file = config['logo_file']
        self.logo_size = config['logo_size']
        self.table_line_h = config['table_line_h']
        self.table_label_w = config['table_label_w']
        self.line_h = config['text_line_h']
        self.indent = config['text_indent']
        self.l_margin = 20
        self.r_margin = 5.0
        self.t_margin = 5.0
        self.b_margin = 10.0
        self.set_auto_page_break(False, self.b_margin)
        self.epw = self.w - self.l_margin - self.r_margin
        self.eph = self.h - self.t_margin - self.b_margin
        self.set_text_color(0, 0, 0)
        self.set_draw_color(0, 0, 0)
        self.set_fill_color(255, 255, 255)
        self.set_font_from_file(config['font_name'], config['font_file'])

    def set_font_from_file(self, font_name, font_file, uni=True):
        """Добавляет новый файл шрифта font_file и устанавливает его с именем font_name"""
        self.add_font(font_name, '', font_file, uni=uni)
        self.set_font(font_name)

    def header(self):
        self.render_version_info()
        self.render_header_table()
        self.render_main_frame()

    def footer(self):
        pass

    def create_page_for_client(self):
        """Создает новую страницу и отрисовывает информацию для клиента"""
        self.add_page()
        # set font
        self.set_font_size(self.font_size_main)

        self.render_text_block(name='Параметры калитки:', 
                               template=INFO_FRAME_FOR_CL, 
                               x=self.l_margin + self.indent,
                               y=self.t_margin + self.line_h * 7,
                               w=self.epw / 2 - self.indent,
                               h=self.line_h)

        self.render_text_block(name='Параметры покраски:', 
                               template=INFO_COLOR, 
                               x=self.l_margin + self.indent,
                               y=self.get_y() + self.line_h,
                               w=self.epw / 2 - self.indent,
                               h=self.line_h)

        self.render_text_block(name='Опции:', 
                               template=INFO_OPTIONS, 
                               x=self.l_margin + self.indent,
                               y=self.get_y() + self.line_h,
                               w=self.epw / 2 - self.indent,
                               h=self.line_h)

        self.render_text_block(name='Примечание:', 
                               template='{comments}', 
                               x=self.l_margin + self.indent,
                               y=self.get_y() + self.line_h,
                               w=self.epw / 2 - self.indent,
                               h=self.line_h)
        
        self.render_text_block(name='Открытие:', 
                               template=INFO_OPEN, 
                               x=self.l_margin + self.epw / 2 + self.indent,
                               y=self.t_margin + self.logo_size,
                               w=self.epw / 2 - self.indent,
                               h=self.line_h)

        self.render_open_view(x=(-self.epw / 6),
                              y=self.t_margin + self.logo_size,
                              w=0,
                              h=self.line_h*3)
        
        self.render_back_view(x=self.l_margin + self.epw / 4 * 3 - 80 / 2,
                                 y=self.t_margin + self.line_h * 7,
                                 w=80,
                                 h=0)

        self.render_frame_view(x=self.l_margin + self.epw / 4 * 3 - 26 / 2,
                                 y=self.t_margin + self.eph - 30,
                                 w=26,
                                 h=0)

    def create_page_for_manufacture(self):
        """Создает новую страницу и отрисовывает информацию для производства"""
        self.add_page()
        # set font size
        self.set_font_size(self.font_size_main)

        self.render_text_block(name='Параметры рамы:', 
                               template=INFO_FRAME_FOR_MAF, 
                               x=self.l_margin + self.epw / 2 + self.indent,
                               y=self.t_margin + self.line_h,
                               w=self.epw / 2 - self.indent * 2,
                               h=self.line_h)
        
        self.render_text_block(name='Параметры створки:', 
                               template=INFO_DOOR, 
                               x=self.l_margin + self.epw / 2 + self.indent,
                               y=self.get_y() + self.line_h,
                               w=self.epw / 2 - self.indent * 2,
                               h=self.line_h)
        
        self.render_text_block(name='Заполнение:', 
                               template=INFO_FILL, 
                               x=self.l_margin + self.epw / 2 + self.indent,
                               y=self.get_y() + self.line_h,
                               w=self.epw / 2 - self.indent * 2,
                               h=self.line_h)
        
        self.render_text_block(name='Параметры покраски:', 
                               template=INFO_COLOR, 
                               x=self.l_margin + self.epw / 2 + self.indent,
                               y=self.get_y() + self.line_h,
                               w=self.epw / 2 - self.indent * 2,
                               h=self.line_h)

        self.render_text_block(name='Опции:', 
                               template=INFO_OPTIONS, 
                               x=self.l_margin + self.epw / 2 + self.indent,
                               y=self.get_y() + self.line_h,
                               w=self.epw / 2 - self.indent * 2,
                               h=self.line_h)

        self.render_text_block(name='Примечание:', 
                               template='{comments}', 
                               x=self.l_margin + self.epw / 2 + self.indent,
                               y=self.get_y() + self.line_h,
                               w=self.epw / 2 - self.indent * 2,
                               h=self.line_h)
        
        self.render_sketch(x=self.l_margin + self.indent,
                           y=self.t_margin + self.table_line_h * 6,
                           h=self.eph - self.table_line_h * 7)

    def save(self, filepath):
        """Сохраняет PDF документ как filepath"""
        self.output(filepath, 'F')

    def render_main_frame(self):
        self.rect(self.l_margin, self.t_margin, self.epw, self.eph)

    def render_version_info(self):
        self.set_font_size(self.font_size_main)
        self.set_xy(self.l_margin, 0)
        self.cell(self.epw, self.t_margin, self.ver, border=0, align='R')

    def render_header_table(self):
        # logo
        self.set_y(self.t_margin)
        x = self.l_margin
        y = self.t_margin
        self.image(self.logo_file, x=x, y=y, w=self.logo_size, h=self.logo_size)
        # set font
        self.set_font_size(self.font_size_header)
        # name plan
        self.cell(self.epw / 2, self.logo_size, 'Калитка ПРЕСТИЖ', border=1, align='C')
        self.ln()
        # set font
        self.set_font_size(self.font_size_main)
        # order
        self.cell(self.table_label_w, self.table_line_h, 
                  'Заказ:', border=1, align='L')
        self.cell(self.epw / 4 - self.table_label_w, self.table_line_h,
                  self.data.get('order'), border=1, align='L')
        # date
        self.cell(self.table_label_w, self.table_line_h, 
                  'Готовность:', border=1, align='L')
        self.cell(self.epw / 4 - self.table_label_w, self.table_line_h,
                  self.data.get('date'), border=1, align='L')
        self.ln()
        # customer
        self.cell(self.table_label_w, self.table_line_h, 
                  'Заказчик:', border=1, align='L')
        self.cell(self.epw / 2 - self.table_label_w, self.table_line_h,
                  self.data.get('customer'), border=1, align='L')
        self.ln()
        # engeener
        self.cell(self.table_label_w, self.table_line_h, 
                  'Инженер:', border=1, align='L')
        self.cell(self.epw / 2 - self.table_label_w, self.table_line_h,
                  self.data.get('engineer'), border=1, align='L')

    def render_text_block(self, name, template, x, y, w=0, h=0, indent=5):
        self.set_xy(x, y)
        self.cell(w, h, name)
        self.ln()
        self.set_x(x + indent)
        self.multi_cell(w - indent, h, template.format(**self.data))

    def render_sketch(self, x, y, w=0, h=0):
        self.set_xy(x, y)
        self.image(self.data['sketch_file'], w=w, h=h)

    def render_open_view(self, x, y, w=0, h=0):
        self.set_xy(x, y)
        self.image(self.data['open_view_file'], w=w, h=h)

    def render_frame_view(self, x, y, w=0, h=0):
        self.set_xy(x, y)
        self.image(self.data['frame_view_file'], w=w, h=h)

    def render_back_view(self, x, y, w=0, h=0):
        self.set_xy(x, y)
        self.image(self.data['back_view_file'], w=w, h=h)

        # width
        string_width = self.get_string_width(self.data['width'])
        self.set_xy(x + w / 2 - string_width / 2, 
                    y - self.line_h / 2)
        self.cell(w=string_width, 
                  h=self.line_h, 
                  txt=self.data['width'], 
                  fill=True)
        
        # height
        string_width = self.get_string_width(self.data['height'])
        self.set_xy(x - string_width, 
                    y + w / 80 * 70)
        self.cell(w=string_width, 
                  h=self.line_h, 
                  txt=self.data['height'], 
                  fill=True)
        
        # cliarance
        string_width = self.get_string_width(self.data['cliarance'])
        self.set_xy(x + w, 
                    y + w / 80 * 122)
        self.cell(w=string_width,
                  h=self.line_h,
                  txt=self.data['cliarance'],
                  fill=True)
        
        #bridge
        if int(self.data['bridge_height']) > 0:
            string_width = self.get_string_width(self.data['bridge_height'])
            self.set_xy(x + w, 
                        y + w / 80 * 20)
            self.cell(w=string_width,
                      h=self.line_h,
                      txt=self.data['bridge_height'],
                      fill=True)
