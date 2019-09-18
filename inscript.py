import os
import textwrap
from typing import List, Tuple

from PIL import Image, ImageFont, ImageDraw, ImageFilter


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
                 font_path: str, message: List[str], angle: float = 0,
                 stroke_offset: int = 4,
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
        self.stroke_offset = stroke_offset
        self.img = self.__create_image()

    @staticmethod
    def __init_stroke_coords(x: int, y: int, offset: int):
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
                __stroke_coords = self.__init_stroke_coords(x, y,
                                                            self.stroke_offset)
                for i in __stroke_coords:
                    draw.multiline_text(i, message, self.stroke_color,
                                        font, align='center')
                # img = img.filter(ImageFilter.GaussianBlur(3))
                # draw = ImageDraw.ImageDraw(img)
                draw.multiline_text((x, y), message, (255, 255, 255),
                                    font, align='center')
                return img


MEMELIB = dict()
FONTS = dict()
basedir_name = os.path.dirname(__file__)
basedir_path = os.path.abspath(basedir_name)


def init_memelib() -> None:
    """
    Initializes the image library from the specified path
    and adds to the dictionary
    """
    listdir = os.listdir('memelib')
    for item in listdir:
        key = item.split('.')[0]
        MEMELIB[key] = basedir_path + r'/memelib/' + item
        print(MEMELIB[key])
        print('Picture {0} found'.format(key))


def init_fonts() -> None:
    """
    Initializes the image library from the specified path
    and adds to the dictionary
    """
    listdir = os.listdir('fonts')
    for item in listdir:
        key = item.split('.')[0]
        FONTS[key] = basedir_path + r'/fonts/' + item
        print(FONTS[key])
        print('Font {0} found'.format(key))


def __image_processing(tag: str = 'kokainum',
                       message: list = ['hello']) -> str:
    """
    The basic function for image processing,
    calls separate methods for different tags
    """
    img = Image.open(MEMELIB[tag])
    img = img.convert('RGBA')
    img_w, img_h = img.size
    center_image_x, center_image_y = img_w // 2, img_h // 2
    if tag == 'kokainum':
        inscription1 = InscriptionImage((450, 150),
                                        (center_image_x, center_image_y + 50),
                                        FONTS['Lobster'],
                                        message[0])
        img = __create_image(img, [inscription1]).convert('RGB')
    if tag == 'wolf':
        inscription1 = InscriptionImage((400, 100),
                                        (center_image_x, center_image_y - 200),
                                        r'fonts/UbuntuMono-Bold.ttf',
                                        message[0])
        img = __create_image(img, [inscription1]).convert('RGB')
    if tag == 'kerildiman':
        inscription1 = InscriptionImage((400, 100),
                                        (center_image_x, center_image_y + 250),
                                        FONTS['Lobster'],
                                        message[0], stroke_offset=7)
        inscription2 = InscriptionImage((400, 100),
                                        (center_image_x, center_image_y - 50),
                                        FONTS['Lobster'],
                                        message[1], stroke_offset=7)
        img = __create_image(img, [inscription1, inscription2]).convert('RGB')
    img.save('meme.png')
    return os.path.abspath('meme.png')


def __create_image(img: Image.Image, inscription: list):
    """The function of adding incriptions to the image"""
    for i in inscription:
        img.paste(i.img,
                  i.t_area_position,
                  i.img)
    return img


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
    return tag, message


def generate_image(query: str):
    tag, message = __parse_query(query)
    result = __image_processing(tag, message)
    return result
