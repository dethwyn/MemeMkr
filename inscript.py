import os
import textwrap
from typing import List, Tuple

from PIL import Image, ImageFont, ImageDraw, ImageFilter

MEME_LIB = {}
FONTS = {}
BASEDIR_NAME = os.path.dirname(__file__)
BASEDIR_PATH = os.path.abspath(BASEDIR_NAME)


class InscriptionImage:
    """
    Class for storage next information:
    - Text's area size (width, height)
    - Text's area position (x, y)
    - Text's font path (str)
    - Message (str)
    - Text slope (degrees, float)
    """

    def __init__(self, t_area_size: Tuple[int, int],
                 t_area_position: Tuple[int, int],
                 font_path: str, message: str, angle: float = 0,
                 stroke_color: Tuple[int, int, int, int] = (
                         0, 0, 0, 255)):
        """ Constructor"""
        self.t_area_size = t_area_size
        x = t_area_position[0] - t_area_size[0] // 2
        y = t_area_position[1] - t_area_size[1] // 2
        self.t_area_position = (x, y)
        self.font_path = font_path
        self.message = message
        self.angle = angle
        self.stroke_color = stroke_color
        self.img = self.__create_image()

    @staticmethod
    def __init_stroke_coords(x: int, y: int):
        offset = [[0, 3], [-2, 2], [-3, 0], [-2, -2], [0, -3], [2, -2], [3, 0]]
        stroke_coords: List[Tuple[int, int]] = []
        for i in offset:
            stroke_coords.append((x + i[0], y + i[1]))
        return stroke_coords

    def __create_image(self) -> Image.Image:
        img = Image.new('RGBA', self.t_area_size, (0, 0, 0, 0))
        draw = ImageDraw.ImageDraw(img)
        font_size = 80
        area_w, area_h = self.t_area_size[0], self.t_area_size[1]
        center_area_x, center_area_y = area_w // 2, area_h // 2
        while True:
            font = ImageFont.truetype(self.font_path, font_size)
            one_symbol_w, one_symbol_h = font.getsize('y')
            max_symbols = area_w // one_symbol_w
            message = textwrap.fill(self.message, max_symbols)
            text_w, text_h = font.getsize_multiline(message)
            if text_h >= area_h - 20:
                font_size -= 2
            else:
                x, y = center_area_x - text_w // 2, center_area_y - text_h // 2
                __stroke_coords = self.__init_stroke_coords(x, y)
                for i in __stroke_coords:
                    draw.multiline_text(i, message, self.stroke_color,
                                        font, align='center')
                draw.multiline_text((x, y), message, (255, 255, 255),
                                    font, align='center')
                return img


def init_memelib() -> None:
    """
    Initializes the image library from the specified path
    and adds to the dictionary
    """
    listdir = os.listdir('memelib')
    for item in listdir:
        key = item.split('.')[0]
        MEME_LIB[key] = BASEDIR_PATH + '\\memelib\\' + item
        print('Picture {0} found'.format(key))


def init_fonts() -> None:
    """
    Initializes the image library from the specified path
    and adds to the dictionary
    """
    listdir = os.listdir('fonts')
    for item in listdir:
        key = item.split('.')[0]
        FONTS[key] = BASEDIR_PATH + '\\fonts\\' + item
        print('Font {0} found'.format(key))


def __image_processing(tag: str = None,
                       message: list = None,
                       name: str = 'meme', ) -> str:
    """
    The basic function for image processing,
    calls separate methods for different tags
    """
    inscript = []
    if tag in MEME_LIB.keys():
        img = Image.open(MEME_LIB[tag])
        img = img.convert('RGBA')
    else:
        blank_size = (300, 150)
        blank_fill = (255, 255, 255, 255)
        img = Image.new('RGBA', blank_size, blank_fill)

    img_w, img_h = img.size
    center_image_x, center_image_y = img_w // 2, img_h // 2

    if tag == 'kokainum':
        area = (450, 150)
        pos = (center_image_x, center_image_y + 120)
        font = FONTS['Lobster']
        text = message[0]
        inscript.append(InscriptionImage(area, pos, font, text))
    elif tag == 'wolf':
        area = (400, 100)
        pos = (center_image_x, center_image_y - 200)
        font = FONTS['Lobster']
        text = message[0]
        inscript.append(InscriptionImage(area, pos, font, text))
    elif tag == 'kerildiman':
        area = (400, 100)
        pos_up = (center_image_x, center_image_y - 50)
        pos_down = (center_image_x, center_image_y + 250)
        font = FONTS['Lobster']
        text_up = message[0]
        text_down = message[1]
        inscript.append(InscriptionImage(area, pos_up, font, text_up))
        inscript.append(InscriptionImage(area, pos_down, font, text_down))
    else:
        area = (290, 140)
        pos = (center_image_x, center_image_y)
        font = FONTS['Lobster']
        text = message[0]
        inscript.append(InscriptionImage(area, pos, font, text))
    for i in inscript:
        img.paste(i.img, i.t_area_position, i.img)
    img.save(name + '.png')
    return os.path.abspath(name + '.png')


def __parse_query(raw_query: str):
    """
    Parses the request submitted as an array of strings
    into a tag and message
    """
    query = raw_query.split('\n')
    tag = query[0].replace(' ', '')
    message = []
    for item in query[1:]:
        message.append(item)
    if not message:
        return tag, ['empty message']
    else:
        return tag, message


def generate_image(query: str, name: str = 'meme'):
    tag, message = __parse_query(query)
    result = __image_processing(tag, message, name)
    return result
