import io
import os

import tornado.ioloop
import tornado.web
from PIL import Image

BASEDIR_NAME = os.path.dirname(__file__)
BASEDIR_PATH = os.path.abspath(BASEDIR_NAME)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class ImageHandler(tornado.web.RequestHandler):
    def get(self, name):
        file_location = os.path.join(BASEDIR_PATH, name + ".png")
        print(file_location)
        if not os.path.isfile(file_location):
            raise tornado.web.HTTPError(status_code=404)

        image = Image.open(file_location)
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        image_string = image_bytes.getvalue()
        self.write(image_string)
        self.set_header("Content-length", len(image_string))
        self.set_header("Content-type", "image/png")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/(.+)", ImageHandler),
    ])


def start_server():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
