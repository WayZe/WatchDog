import emojis
import telebot
import logging
from parser import Rater
from typing import Dict, Union
from functions import get_str_env, get_int_env

bot = telebot.TeleBot(get_str_env('TOKEN'))

rater = Rater()
currencies_to_rates: Dict[str, Dict[str, Union[str, float]]] = rater.currencies_data
text: str = ''
for currency, rate_emoji in currencies_to_rates.items():
    text = text + emojis.encode(f"{rate_emoji['emoji']} Курс {currency} {rate_emoji['rate']}\n")
bot.send_message(get_int_env('MY_ID'), text)
logging.warning(f"Отправлено оповещение пользователю {get_int_env('MY_ID')}.")
