import emojis
import telebot
import logging
from parser import Rater
from celery import Celery
from typing import Dict, Union
from celery.schedules import crontab
from postgres_storage import PostgresStorage
from functions import get_str_env, get_int_env


rater = Rater()
postgres_storage = PostgresStorage()
redis_url: str = get_str_env('REDIS_URL')
bot = telebot.TeleBot(get_str_env('TOKEN'))
celery = Celery('periodic', broker=redis_url)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=7, minute = 0), send_notification.s(), name='notification')


@celery.task
def send_notification():
    text: str = ''
    currencies_to_rates: Dict[str, Dict[str, Union[str, float]]] = rater.currencies_data
    for currency, rate_emoji in currencies_to_rates.items():
        text = text + emojis.encode(f"{rate_emoji['emoji']} Курс {currency} {rate_emoji['rate']}\n")

    user_ids = postgres_storage.get_user_ids_to_notify()
    for user_id in user_ids:
        bot.send_message(user_id, text)
        logging.warning(f"Отправлено оповещение пользователю {user_id}.")
