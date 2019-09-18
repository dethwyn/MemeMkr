import os
import logging
from uuid import uuid4
import multiprocessing

from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.utils.helpers import escape_markdown
from dotenv import load_dotenv

from inscript import generate_image, init_fonts, init_memelib
import tornado_server

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    MEME_PATH = generate_image(query)
    print(MEME_PATH)
    """
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Caps",
            input_message_content=InputTextMessageContent(
                query.upper())),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Bold",
            input_message_content=InputTextMessageContent(
                "*{}*".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent(
                "_{}_".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN))]

    update.inline_query.answer(results)
    """


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def start_bot():
    init_memelib()
    init_fonts()
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
    print(request_kwargs)
    updater = Updater(token, use_context=True, request_kwargs=request_kwargs)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(InlineQueryHandler(inlinequery))

    dp.add_error_handler(error)
    print('starting bot...')
    updater.start_polling()
    updater.idle()


def start_server():
    print('starting server...')
    tornado_server.start_server()


if __name__ == '__main__':
    # main()
    # p = multiprocessing.Process(target=start_server)
    # p.start()
    start_bot()
