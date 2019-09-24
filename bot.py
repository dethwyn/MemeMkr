import logging
import os
from uuid import uuid4

from dotenv import load_dotenv
from telegram import InlineQueryResultCachedPhoto, InlineQueryResultArticle, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler

from inscript import generate_image
import app_var
from app_var import CHANEL_ID, HELP_STRING, BASEDIR_PATH, MEME_LIB, FONTS

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


class MemeMkrBot:
    def __init__(self):
        load_dotenv()
        token = os.getenv('TOKEN')
        # proxy_url = os.getenv('PROXY_URL')
        # proxy_username = os.getenv('PROXY_USERNAME')
        # proxy_password = os.getenv('PROXY_PASSWORD')
        # request_kwargs = {
        #     'proxy_url': proxy_url,
        #     'urllib3_proxy_kwargs': {
        #         'username': proxy_username,
        #         'password': proxy_password,
        #     }
        # }
        self.updater = Updater(token, use_context=True)

        self.dp = self.updater.dispatcher
        self.dp.add_handler(CommandHandler('tags', self.get_tags))
        self.dp.add_handler(CommandHandler('start', self.start_command))
        self.dp.add_handler(CommandHandler('help', self.help_command))
        self.dp.add_handler(InlineQueryHandler(self.inlinequery))

        self.dp.add_error_handler(self.error)

    def start(self):
        logger.info('The bot is running')
        self.updater.start_polling()
        self.updater.idle()

    def start_command(self, update, context):
        """Send a message when the command /start is issued."""
        update.message.reply_text('Hi!')

    def help_command(self, update, context):
        """Send a message when the command /help is issued."""
        update.message.reply_text(HELP_STRING)

    def get_help_string(self):
        answer = [InlineQueryResultArticle(
            id=uuid4(),
            title=HELP_STRING,
            input_message_content=InputTextMessageContent('ы'))]
        return answer

    def get_tags(self, update, context):

        update.message.reply_text(app_var.TAGS_STRING)

    def error(self, update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def inlinequery(self, update, context):
        """Handle the inline query."""
        query = update.inline_query.query
        results = self.get_picture(update, query)
        update.inline_query.answer(results)

    def get_picture(self, update, query):
        logger.info('input query ' + query)
        results = []
        if query == '':
            for key in MEME_LIB:
                answer = InputTextMessageContent(key)
                results.append(InlineQueryResultArticle(id=uuid4(), title=key,
                                                        input_message_content=answer))

        else:
            name = update.inline_query.from_user['username']
            meme_path = generate_image(query, '{0}{1}'.format(name, 'IMG'))
            msg = self.updater.bot.send_photo(chat_id=CHANEL_ID,
                                              photo=open(meme_path, "rb"))
            file_id = msg.photo[0].file_id
            self.updater.bot.delete_message(chat_id=CHANEL_ID,
                                            message_id=msg.message_id)
            results.append(InlineQueryResultCachedPhoto(id=uuid4(),
                                                        photo_file_id=file_id))
        return results

    @staticmethod
    def init_tags_string():
        app_var.TAGS_STRING = 'Kokainum tags: '
        for s in app_var.KOKAINUM_TAGS:
            app_var.TAGS_STRING += s
            app_var.TAGS_STRING += '; '
        app_var.TAGS_STRING += '\n'

        app_var.TAGS_STRING += 'Sandman tags: '
        for s in app_var.SANDMAN_TAGS:
            app_var.TAGS_STRING += s
            app_var.TAGS_STRING += '; '
        app_var.TAGS_STRING += '\n'

        app_var.TAGS_STRING += 'Girls + cat tags: '
        for s in app_var.CATGIRLS_TAGS:
            app_var.TAGS_STRING += s
            app_var.TAGS_STRING += '; '
        app_var.TAGS_STRING += '\n'

        app_var.TAGS_STRING += 'Brain tags: '
        for s in app_var.BRAIN_TAGS:
            app_var.TAGS_STRING += s
            app_var.TAGS_STRING += '; '
        app_var.TAGS_STRING += '\n'

        app_var.TAGS_STRING += 'Crying cat tags: '
        for s in app_var.CRYING_TAGS:
            app_var.TAGS_STRING += s
            app_var.TAGS_STRING += '; '
        app_var.TAGS_STRING += '\n'

    @staticmethod
    def init_meme_lib() -> None:
        """
        Initializes the image library from the specified path
        and adds to the dictionary
        :return: None
        """
        listdir = os.listdir('memelib')
        for item in listdir:
            key = item.split('.')[0]
            MEME_LIB[key] = BASEDIR_PATH + '/memelib/' + item
            logger.info('Picture {0} found'.format(key))

    @staticmethod
    def init_fonts() -> None:
        """
        Initializes the image library from the specified path
        and adds to the dictionary
        :return: None
        """
        listdir = os.listdir('fonts')
        for item in listdir:
            key = item.split('.')[0]
            FONTS[key] = BASEDIR_PATH + '/fonts/' + item
            logger.info('Font {0} found'.format(key))


if __name__ == '__main__':
    MemeMkrBot.init_meme_lib()
    MemeMkrBot.init_fonts()
    MemeMkrBot.init_tags_string()
    bot = MemeMkrBot()
    bot.start()
