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
        stroke_coords: List[Tuple[int, int]] = []
        for i in range(1, offset + 1):
            stroke_coords.append((x - i, y))
            stroke_coords.append((x + i, y))
            stroke_coords.append((x, y + i))
            stroke_coords.append((x, y - i))
            stroke_coords.append((x - i, y - i))
            stroke_coords.append((x + i, y + i))
            stroke_coords.append((x - i, y + i))
            stroke_coords.append((x + i, y - i))
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
                img = img.filter(ImageFilter.GaussianBlur(3))
                draw = ImageDraw.ImageDraw(img)
                draw.multiline_text((x, y), message, (255, 255, 255),
                                    font, align='center')
                return img
