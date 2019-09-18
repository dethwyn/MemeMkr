# 352593518

import logging
import os
from uuid import uuid4

from dotenv import load_dotenv
from telegram import InlineQueryResultCachedPhoto
from telegram.ext import Updater, InlineQueryHandler, CommandHandler

from inscript import generate_image, init_fonts, init_memelib

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


class MemeMkrBot:
    def __init__(self):
        load_dotenv()
        token = os.getenv('TOKEN')
        proxy_url = os.getenv('PROXY_URL')
        proxy_username = os.getenv('PROXY_USERNAME')
        proxy_password = os.getenv('PROXY_PASSWORD')
        request_kwargs = {
            'proxy_url': proxy_url,
            'urllib3_proxy_kwargs': {
                'username': proxy_username,
                'password': proxy_password,
            }
        }
        self.updater = Updater(token, use_context=True,
                               request_kwargs=request_kwargs)

        self.dp = self.updater.dispatcher

        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(CommandHandler("help", self.help))
        self.dp.add_handler(InlineQueryHandler(self.inlinequery))

        self.dp.add_error_handler(self.error)

        print('starting bot...')
        self.updater.start_polling()
        self.updater.idle()

    def start(self, update, context):
        """Send a message when the command /start is issued."""
        update.message.reply_text('Hi!')

    def help(self, update, context):
        """Send a message when the command /help is issued."""
        update.message.reply_text('Help!')

    def inlinequery(self, update, context):
        """Handle the inline query."""
        query = update.inline_query.query
        msg = self.updater.bot.send_message(chat_id='352593518', text='test')
        self.updater.bot.delete_message(chat_id='352593518',
                                        message_id=msg.message_id)
        name = msg.chat['username']
        MEME_PATH = generate_image(query, name)
        msg = self.updater.bot.send_photo(chat_id='352593518',
                                          photo=open(MEME_PATH, "rb"))
        file_id = msg.photo[0].file_id
        self.updater.bot.delete_message(chat_id='352593518',
                                        message_id=msg.message_id)

        results = [
            InlineQueryResultCachedPhoto(
                id=uuid4(),
                photo_file_id=file_id,
            )]

        update.inline_query.answer(results)

    def error(self, update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)


"""
def start_bot():
    init_memelib()
    init_fonts()

    token = os.getenv('TOKEN')
    proxy_url = os.getenv('PROXY_URL')
    proxy_username = os.getenv('PROXY_USERNAME')
    proxy_password = os.getenv('PROXY_PASSWORD')
    request_kwargs = {
        'proxy_url': proxy_url,
        'urllib3_proxy_kwargs': {
            'username': proxy_username,
            'password': proxy_password,
        }
    }
    print(request_kwargs)
    UPDATER = Updater(token, use_context=True, request_kwargs=request_kwargs)

    # UPDATER.bot.send_photo('352593518', file)
    dp = UPDATER.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(InlineQueryHandler(inlinequery))

    dp.add_error_handler(error)

    print('starting bot...')
    UPDATER.start_polling()
    UPDATER.idle()
"""

if __name__ == '__main__':
    # main()
    # p = multiprocessing.Process(target=start_server)
    # p.start()
    init_memelib()
    init_fonts()
    bot = MemeMkrBot()
