"""
Module for parsing the request of the integrated telegram bot.
Parses a request for a tag and an message.
The tag serves to select an image, the message adds to the image.
"""
import os

from PIL import Image

from inscript import InscriptionImage

MEMELIB = dict()
FONTS = dict()


def init_memelib() -> None:
    """
    Initializes the image library from the specified path
    and adds to the dictionary
    """
    listdir = os.listdir('memelib')
    for item in listdir:
        key = item.split('.')[0]
        MEMELIB[key] = r'memelib\{0}'.format(item)
        print('Picture {0} found'.format(key))


def init_fonts() -> None:
    """
    Initializes the image library from the specified path
    and adds to the dictionary
    """
    listdir = os.listdir('fonts')
    for item in listdir:
        key = item.split('.')[0]
        FONTS[key] = r'fonts\{0}'.format(item)
        print('Font {0} found'.format(key))


def __image_processing(tag: str = 'kokainum', message: list = ['hello']) -> str:
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
    img.save('meme.jpg')
    return os.path.abspath('meme.jpg')


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
    print(result)
