import logging
import os
from uuid import uuid4

from dotenv import load_dotenv
from telegram import InlineQueryResultCachedPhoto, InlineQueryResultArticle, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler

from inscript import generate_image, init_fonts, init_meme_lib
from global_var import CHANEL_ID, HELP_STRING

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
        update.message.reply_text(HELP_STRING)

    def get_help_string(self):
        answer = [InlineQueryResultArticle(
            id=uuid4(),
            title=HELP_STRING,
            input_message_content=InputTextMessageContent(''))]
        return answer

    def inlinequery(self, update, context):
        """Handle the inline query."""
        query = update.inline_query.query
        if query.lower() == 'help':
            results = self.get_help_string()
        else:
            results = self.get_picture(update, query)
        update.inline_query.answer(results)

    def error(self, update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def get_picture(self, update, query):
        name = update.inline_query.from_user['username']
        meme_path = generate_image(query, '{0}{1}'.format(name, 'IMG'))
        msg = self.updater.bot.send_photo(chat_id=CHANEL_ID,
                                          photo=open(meme_path, "rb"))
        file_id = msg.photo[0].file_id
        self.updater.bot.delete_message(chat_id=CHANEL_ID,
                                        message_id=msg.message_id)
        results = [
            InlineQueryResultCachedPhoto(
                id=uuid4(),
                photo_file_id=file_id,
            )]
        return results


if __name__ == '__main__':
    init_meme_lib()
    init_fonts()
    bot = MemeMkrBot()
