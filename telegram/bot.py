import http.client
import json
import logging
import logging.config
import urllib.parse
import yaml

from telegram.ext import Updater, CommandHandler

import settings


# Init logging
with open('logging.yaml', 'rt') as f:
    config = yaml.safe_load(f.read())
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)


def request_subreddits_data(bot, update, args):
    # type: (telegram.ext.Bot, telegram.ext.Update) -> None
    """Request reddit Spider data."""
    logger.info('Request Spider Data')
    conn = http.client.HTTPConnection(settings.SCRAPPY_COCO_URL,
                                      settings.SCRAPPY_COCO_PORT)

    # build URL
    subreddits = args[0]
    params = urllib.parse.urlencode({'spider_name': 'reddit',
                                     'start_requests': True,
                                     'subreddits': subreddits})
    url = '/crawl.json?' + params
    conn.request('GET', url)
    logger.debug('URL: %s', url)

    # request data
    response = conn.getresponse()
    response_data = response.read().decode('utf-8')

    # reply user message
    send_telegram_message(bot, update, json.loads(response_data))


def send_telegram_message(bot, update, data):
    # type: (telegram.ext.Bot, telegram.ext.Update, dict[str, Any]) -> None
    logger.info('Send Telegram Message')
    for thread in data['items']:
        bot.send_message(chat_id=update.message.chat.id,
                         text=thread,
                         reply_to_message_id=update.message.message_id)
    else:
        logger.info('There are\'t items to send')


# set bot commands
updater = Updater(settings.TELEGRAM_TOKEN)
updater.dispatcher.add_handler(
    CommandHandler('nada_pra_fazer', request_subreddits_data, pass_args=True)
)

# start pooling messages
updater.start_polling()
updater.idle()
