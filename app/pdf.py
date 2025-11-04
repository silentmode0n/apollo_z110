from fpdf import (
    FPDF,
    FontFace,
    )
from .config import (
    CAP_TITLE,
    COMMENT_TITLE,
    FENCE_TITLE,
    FONT_FILEPATH,
    FONT_B_FILEPATH,
    FONT_NAME,
    LAMEL_TITLE,
    LOGO_FILEPATH,
    RAIL_TITLE,
    SLAT_TITLE,
    TITLE,
    VERSION,
    )


BLACK = (0, 0, 0)
RED = (250, 0, 0)
GREY = (188, 188, 188)
WHITE = (255, 255, 255)

FONT_MAIN_SIZE = 10
FONT_TITLE_SIZE = 16
ROW_H = 6
LOGO_SIZE = ROW_H * 2
HEADER_LABEL_W = 24
TABLE_HEADER_H = 7


class PDF(FPDF):
    def __init__(self, data):
        super().__init__('P', 'mm', 'A4')
        self.data = data
        self.l_margin = 20
        self.r_margin = 5.0
        self.t_margin = 5.0
        self.b_margin = 10.0
        self.set_auto_page_break(True, self.b_margin)
        self.set_text_color(*BLACK)
        self.set_draw_color(*BLACK)
        self.add_font(FONT_NAME, '', FONT_FILEPATH)
        self.add_font(FONT_NAME, 'B', FONT_B_FILEPATH)
        self.set_font(FONT_NAME, style='')

    def save(self, filepath):
        """Сохраняет PDF документ как filepath"""
        self.output(filepath)

    def header(self):
        self.render_version_info()
        self.render_header_table()

    def footer(self):
        self.render_main_frame()

    def render_main_frame(self):
        self.rect(self.l_margin, self.t_margin, self.epw, self.eph)

    def render_version_info(self):
        self.set_font_size(FONT_MAIN_SIZE)
        self.set_xy(self.l_margin, 0)
        self.cell(self.epw, self.t_margin, VERSION, border=0, align='R')

    def render_header_table(self):
        # render logo
        self.set_y(self.t_margin)
        self.image(LOGO_FILEPATH, x=self.l_margin, y=self.t_margin, w=LOGO_SIZE, h=LOGO_SIZE)
        # set font
        self.set_font_size(FONT_TITLE_SIZE)
        # name plan
        self.cell(self.epw / 2, LOGO_SIZE, TITLE, border=0, align='C')
        # set font
        self.set_font_size(FONT_MAIN_SIZE)
        # print order row
        self.cell(HEADER_LABEL_W, ROW_H, 
                  'Заказ:', border=1, align='L')
        self.cell(self.epw / 2 - HEADER_LABEL_W, ROW_H,
                  self.data['order_info']['order'], border=1, align='L')
        # print date row
        self.ln()
        self.cell(self.epw / 2, ROW_H) #blank
        self.cell(HEADER_LABEL_W, ROW_H, 
                  'Дата:', border=1, align='L')
        self.cell(self.epw / 2 - HEADER_LABEL_W, ROW_H,
                  self.data['order_info']['date'], border=1, align='L')
        self.ln()
        # customer
        self.cell(HEADER_LABEL_W, ROW_H, 
                  'Заказчик:', border=1, align='L')
        self.cell(self.epw / 2 - HEADER_LABEL_W, ROW_H,
                  self.data['order_info']['customer'], border=1, align='L')
        # engeener
        self.cell(HEADER_LABEL_W, ROW_H, 
                  'Инженер:', border=1, align='L')
        self.cell(self.epw / 2 - HEADER_LABEL_W, ROW_H,
                  self.data['order_info']['engineer'], border=1, align='L')
        self.ln()
        self.ln()

    def draw_table(self, headings: list, rows: list, width: int, col_widths: tuple, align: str):
        self.set_font_size(FONT_MAIN_SIZE)
        # headings_style = FontFace(fill_color=GREY)
        table_data = [headings,] + rows

        with self.table(
            align=align,
            width=width,
            text_align=('LEFT', 'LEFT', 'CENTER', 'CENTER'),
            col_widths=col_widths,
            # headings_style=headings_style,
            borders_layout="SINGLE_TOP_LINE") as table:
            for data_row in table_data:
                table.row(data_row)

    def draw_table_name(self, txt, width, align):
        self.set_font(style='B')
        if align == 'LEFT':
            self.cell(width, ROW_H, txt)
        elif align == 'RIGHT':
            self.cell(self.epw - width)
            self.cell(width, ROW_H, txt)
        self.ln()
        self.set_font(style='')

    def render_fences(self, width, align):
        headings = ['Размер', 'Цвет', 'Секций', 'Планок по']
        rows = [(
            fence['width'] + 'x' + fence['height'], 
            fence['color'] + ' ' + fence['colortype'], 
            fence['count'],
            fence['slat_num']
            ) for fence in self.data['fences']]
        self.draw_table_name(f'{FENCE_TITLE}:', width, 'LEFT')
        self.draw_table(headings, rows, int(width), (1, 1.3, 0.8, 0.9), align)
        self.ln()

    def render_lamels(self, width, align):
        headings = ['Размер', 'Цвет', 'шт']
        rows = [(
            lamel['size'], 
            lamel['color'] + ' ' + lamel['colortype'], 
            lamel['count']
            ) for lamel in self.data['lamels']]
        self.draw_table_name(f'{LAMEL_TITLE}:', width, align)
        self.draw_table(headings, rows, int(width), (1, 1, 0.5), align)
        self.ln()

    def render_rails(self, width, align):
        headings = ['Размер', 'Цвет', 'пара']
        rows = [(
            rail['size'], 
            rail['color'] + ' ' + rail['colortype'], 
            rail['count']
            ) for rail in self.data['rails']]
        self.draw_table_name(f'{RAIL_TITLE}:', width, align)
        self.draw_table(headings, rows, int(width), (1, 1, 0.5), align)
        self.ln()

    def render_caps(self, width, align):
        headings = ['Размер', 'Цвет', 'шт']
        rows = [(
            cap['size'], 
            cap['color'] + ' ' + cap['colortype'], 
            cap['count']
            ) for cap in self.data['caps']]
        self.draw_table_name(f'{CAP_TITLE}:', width, align)
        self.draw_table(headings, rows, int(width), (1, 1, 0.5), align)
        self.ln()

    def render_slats(self, width, align):
        headings = ['Размер', 'Цвет', 'шт']
        rows = [(
            slat['size'], 
            slat['color'] + ' ' + slat['colortype'], 
            slat['count']
            ) for slat in self.data['slats']]
        self.draw_table_name(f'{SLAT_TITLE}:', width, align)
        self.draw_table(headings, rows, int(width), (1, 1, 0.5), align)
        self.ln()

    def render_comments(self, width, align):
        self.draw_table_name(f'{COMMENT_TITLE}:', width, align)
        align = 'L' if align == 'LEFT' else 'R'
        if align == 'R':
            self.ln(self.epw - width)
        self.multi_cell(width, None, self.data['comments'], align=align)
        self.ln()

    def create_page(self):
        self.add_page()
        self.set_font_size(FONT_MAIN_SIZE)
        self.set_y(FONT_MAIN_SIZE * 3)
        self.render_fences(self.epw / 2 + 10, 'LEFT')
        self.render_comments(self.epw / 2 +10, 'LEFT')
        self.set_y(FONT_MAIN_SIZE * 3)
        self.render_lamels(self.epw / 2 - 20, 'RIGHT')
        self.render_rails(self.epw / 2 - 20, 'RIGHT')
        self.render_caps(self.epw / 2 - 20, 'RIGHT')
        self.render_slats(self.epw / 2 - 20, 'RIGHT')

