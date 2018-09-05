import logging

from telegram.ext import Updater, CommandHandler

from settings import TELEGRAM_TOKEN


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


updater = Updater(TELEGRAM_TOKEN)

updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.start_polling()
updater.idle()