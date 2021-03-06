import os
import textwrap
from typing import List, Tuple

from PIL import Image, ImageFont, ImageDraw

import app_var
from app_var import MEME_LIB, FONTS


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
                 font_path: str,
                 message: str,
                 type: int = 0,
                 angle: float = 0,
                 text_align: str = 'center',
                 stroke_color: Tuple[int, int, int, int] = (0, 0, 0, 255),
                 font_color: Tuple[int, int, int, int] = (255, 255, 255, 255)):
        """ Constructor"""
        self.t_area_size = t_area_size
        x = t_area_position[0] - t_area_size[0] // 2
        y = t_area_position[1] - t_area_size[1] // 2
        self.t_area_position = (x, y)
        self.font_path = font_path
        self.message = message
        self.angle = angle
        self.text_align = text_align
        self.stroke_color = stroke_color
        self.font_color = font_color
        if type == 0:
            self.img = self.__create_inscription()
        elif type == 1:
            self.img = self.__create_candle_inscription()

    @staticmethod
    def __init_stroke(x: int, y: int) -> List[Tuple[int, int]]:
        offset = [[0, 3], [-2, 2], [-3, 0], [-2, -2], [0, -3], [2, -2], [3, 0]]
        stroke_coords = []
        for i in offset:
            stroke_coords.append((x + i[0], y + i[1]))
        return stroke_coords

    def __create_inscription(self) -> Image.Image:
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
            if text_h >= area_h - 15 or text_w >= area_w - 5:
                font_size -= 2
            else:
                x, y = center_area_x - text_w // 2, center_area_y - text_h // 2
                stroke_coords = self.__init_stroke(x, y)
                for i in stroke_coords:
                    draw.multiline_text(i, message, self.stroke_color,
                                        font, align=self.text_align)
                draw.multiline_text((x, y), message, self.font_color,
                                    font, align=self.text_align)

                return img

    def __create_candle_inscription(self):
        img = Image.new('RGBA', self.t_area_size, (0, 0, 0, 0))
        draw = ImageDraw.ImageDraw(img)
        font_size = 30
        font = ImageFont.truetype(self.font_path, font_size)
        one_symbol_w, one_symbol_h = font.getsize('y')
        max_symbols = 200 // one_symbol_w
        wrap_string = textwrap.fill(self.message, max_symbols)
        # str2 = self.message[max_symbols:len(self.message)]
        # max_symbols = 300 // one_symbol_w
        # str2 = textwrap.fill(str2, max_symbols)
        list_string = wrap_string.split('\n')

        draw.multiline_text((120, 0), list_string[0], self.font_color,
                            font, align=self.text_align)
        second_string = ''
        for item in list_string[1:len(list_string)]:
            second_string += item + '\n'
        draw.multiline_text((0, 40), second_string, self.font_color,
                            font, align=self.text_align)
        return img


def __parse_tag(tag: str, len_message: int) -> str:
    if tag in app_var.KOKAINUM_TAGS:
        tag = 'kokainum'
    elif tag in app_var.SANDMAN_TAGS:
        tag = 'sandman'
    elif tag in app_var.CATGIRLS_TAGS:
        tag = 'girlscat'
    elif tag in app_var.WOLF_TAGS:
        tag = 'wolf'
    elif tag in app_var.BOYFRIEND_TAGS:
        tag = 'boyfriend'
    elif tag in app_var.BRAIN_TAGS:
        if len_message == 3:
            tag = 'brain3'
        elif len_message == 4:
            tag = 'brain4'
        elif len_message >= 5:
            tag = 'brain5'
        else:
            tag = 'brain3'
    elif tag in app_var.CRYING_TAGS:
        tag = 'crying'
    elif tag in app_var.TORERO_TAGS:
        tag = 'torero'
    elif tag in app_var.CANDLE_TAGS:
        tag = 'candle'
    elif tag in app_var.PETROSYAN_TAGS:
        tag = 'petrosyan'
    else:
        tag = 'blank'
    return tag


def __image_processing(tag: str = None,
                       message: list = None,
                       name: str = 'meme', ) -> str:
    """
    The basic function for image processing.
    If tag is empty creates a blank white image with the inscription
    If message is empty creates image with inscription 'empy message'
    :param tag: name of image
    :param message: list of messages
    :param name: file name
    :return: abs path to saved image
    """
    tag = __parse_tag(tag, len(message))
    inscript = []
    for _ in range(0, 10 - len(message)):
        message.append('message')
    # if not message:
    # message = ['message' for i in range(10)]
    if tag in MEME_LIB.keys():
        img = Image.open(MEME_LIB[tag])
        img = img.convert('RGBA')
    else:
        blank_size = (300, 150)
        blank_fill = (255, 255, 255, 255)
        img = Image.new('RGBA', blank_size, blank_fill)

    img_w, img_h = img.size
    center_x, center_y = img_w // 2, img_h // 2
    font = FONTS['Impact']
    if tag == 'kokainum':
        area = (450, 150)
        pos = (center_x, center_y + 120)
        text = message[0]
        inscript.append(InscriptionImage(area, pos, font, text))
    elif tag == 'wolf':
        area = (400, 100)
        pos = (center_x, center_y - 120)
        text = message[0]
        inscript.append(InscriptionImage(area, pos, font, text))
    elif tag == 'sandman':
        area = (300, 100)
        pos_up = (center_x, center_y - 220)
        pos_down = (center_x, center_y + 200)
        text_up = message[0]
        text_down = message[1]
        inscript.append(InscriptionImage(area, pos_up, font, text_up))
        inscript.append(InscriptionImage(area, pos_down, font, text_down))
    elif tag == 'girlscat':
        area = (390, 150)
        pos_left = (center_x - center_x // 2, center_y + 120)
        pos_right = (center_x + center_x // 2, center_y + 120)
        text_up = message[0]
        text_down = message[1]
        inscript.append(InscriptionImage(area, pos_left, font, text_up))
        inscript.append(InscriptionImage(area, pos_right, font, text_down))
    elif tag == 'boyfriend':
        area_left = (170, 120)
        pos_left = (180, 230)
        text_left = message[0]

        area_center = (150, 110)
        pos_center = (380, 150)
        text_center = message[1]

        area_right = (150, 120)
        pos_right = (500, 230)
        text_right = message[2]
        inscript.append(
            InscriptionImage(area_left, pos_left, font, text_left))
        inscript.append(
            InscriptionImage(area_center, pos_center, font, text_center))
        inscript.append(
            InscriptionImage(area_right, pos_right, font, text_right))
    elif tag == 'brain5':
        area = (450, 200)
        pos_1 = (240, 105)
        text_1 = message[0]
        pos_2 = (240, 315)
        text_2 = message[1]
        pos_3 = (240, 530)
        text_3 = message[2]
        pos_4 = (240, 730)
        text_4 = message[3]
        pos_5 = (240, 940)
        text_5 = message[4]
        inscript.append(InscriptionImage(area, pos_1, font, text_1))
        inscript.append(InscriptionImage(area, pos_2, font, text_2))
        inscript.append(InscriptionImage(area, pos_3, font, text_3))
        inscript.append(InscriptionImage(area, pos_4, font, text_4))
        inscript.append(InscriptionImage(area, pos_5, font, text_5))
    elif tag == 'brain3':
        area = (450, 200)
        pos_1 = (240, 105)
        text_1 = message[0]
        pos_2 = (240, 315)
        text_2 = message[1]
        pos_3 = (240, 530)
        text_3 = message[2]
        inscript.append(InscriptionImage(area, pos_1, font, text_1))
        inscript.append(InscriptionImage(area, pos_2, font, text_2))
        inscript.append(InscriptionImage(area, pos_3, font, text_3))
    elif tag == 'brain4':

        area = (450, 200)
        pos_1 = (240, 105)
        text_1 = message[0]
        pos_2 = (240, 315)
        text_2 = message[1]
        pos_3 = (240, 530)
        text_3 = message[2]
        pos_4 = (240, 730)
        text_4 = message[3]
        inscript.append(InscriptionImage(area, pos_1, font, text_1))
        inscript.append(InscriptionImage(area, pos_2, font, text_2))
        inscript.append(InscriptionImage(area, pos_3, font, text_3))
        inscript.append(InscriptionImage(area, pos_4, font, text_4))
    elif tag == 'crying':
        area = (700, 170)
        pos = (center_x, center_y + 130)
        text = message[0]
        inscript.append(InscriptionImage(area, pos, font, text))
    elif tag == 'torero':
        area = (290, 95)
        pos_1 = (150, 42)
        text_1 = message[0]
        pos_2 = (150, 137)
        text_2 = message[1]
        pos_3 = (150, 232)
        text_3 = message[2]
        pos_4 = (150, 327)
        text_4 = message[3]
        inscript.append(InscriptionImage(area, pos_1, font, text_1))
        inscript.append(InscriptionImage(area, pos_2, font, text_2))
        inscript.append(InscriptionImage(area, pos_3, font, text_3))
        inscript.append(InscriptionImage(area, pos_4, font, text_4))
    elif tag == 'candle':
        area = (320, 150)
        pos = (330, 200)
        text = message[0]
        inscript.append(InscriptionImage(area, pos, font, text,
                                         type=1,
                                         text_align='left',
                                         font_color=(170, 110, 60, 255)))
    elif tag == 'petrosyan':
        area = (500, 120)
        pos = (250, 540)
        text = message[0]
        inscript.append(InscriptionImage(area,
                                         pos,
                                         font,
                                         text))
    else:
        area = (320, 150)
        pos = (center_x, center_y)
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
    :param raw_query: query from the bot
    :return: tag - string with name of meme, message - list of messages
    """
    query = raw_query.split('\n')
    tag = query[0].replace(' ', '')
    message = []
    for item in query[1:]:
        message.append(item)
    return tag.lower(), message


def generate_image(query: str, name: str = 'meme'):
    """
    Main function to generation image with inscriptions
    :param query: query from bot
    :param name: file name when saving
    :return: abs path to the file
    """
    tag, message = __parse_query(query)
    result = __image_processing(tag, message, name)
    return result
