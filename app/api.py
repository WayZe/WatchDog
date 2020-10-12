import os
import emojis
import telebot
import logging
from parser import Rater
from typing import Dict, Union
from functions import get_str_env


bot = telebot.TeleBot(get_str_env('TOKEN'))


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        r'Введите /currencies для получения курса валют.'
    )
    logging.warning('Пользователь нажал кнопку start.')


@bot.message_handler(commands=['currencies'])
def currency_message(message):
    rater = Rater()
    currencies_to_rates: Dict[str, Dict[str, Union[str, float]]] = rater.get_all()
    text: str = ''
    for currency, rate_emoji in currencies_to_rates.items():
        text = text + emojis.encode(f"{rate_emoji['emoji']} Курс {currency} {rate_emoji['rate']}\n")
    bot.send_message(
        message.chat.id,
        text
    )
    logging.warning('Пользователь нажал кнопку currencies.')





bot.polling()
