import http.client
import json
import logging
import urllib.parse

from telegram.ext import Updater, CommandHandler

import settings


def request_spider_data(bot, update):
    # type: (telegram.ext.Bot, telegram.ext.Update) -> None
    """Request reddit Spider data."""
    logging.info('Request Spider Data')
    conn = http.client.HTTPConnection(settings.SCRAPPY_COCO_URL,
                                      settings.SCRAPPY_COCO_PORT)
    params = urllib.parse.urlencode({'spider_name': 'reddit',
                                     'start_requests': True})
    conn.request('GET', '/crawl.json?' + params)

    response = conn.getresponse()
    response_data = response.read().decode('utf-8')

    send_telegram_message(bot, update, json.loads(response_data))


def send_telegram_message(bot, update, data):
    # type: (telegram.ext.Bot, telegram.ext.Update, dict[str, Any]) -> None
    logging.info('Send Telegram Message')
    logging.debug(data)
    for thread in data['items']:
        bot.send_message(chat_id=update.message.chat.id,
                         text=thread,
                         reply_to_message_id=update.message.message_id)


# set bot commands
updater = Updater(settings.TELEGRAM_TOKEN)
updater.dispatcher.add_handler(
    CommandHandler('nada_pra_fazer', request_spider_data)
)

# start pooling messages
updater.start_polling()
updater.idle()
