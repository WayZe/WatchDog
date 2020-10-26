import emojis
import telebot
import logging
from parser import Rater
from celery import Celery
from typing import Dict, Union
from celery.schedules import crontab
from functions import get_str_env, get_int_env


redis_url: str = get_str_env('REDIS_URL')
celery = Celery('notification', broker=redis_url)
bot = telebot.TeleBot(get_str_env('TOKEN'))
admin_id = get_int_env('ADMIN_ID')
rater = Rater()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=7, minute=0), test.s(), name='notification')


@celery.task
def test():
    currencies_to_rates: Dict[str, Dict[str, Union[str, float]]] = rater.currencies_data
    text: str = ''
    for currency, rate_emoji in currencies_to_rates.items():
        text = text + emojis.encode(f"{rate_emoji['emoji']} Курс {currency} {rate_emoji['rate']}\n")
    bot.send_message(admin_id, text)
    logging.warning(f"Отправлено оповещение пользователю {admin_id}.")
