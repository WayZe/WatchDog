import emojis
import telebot
import logging
from parser import Rater
from typing import Dict, Union
from functions import get_str_env, get_int_env


bot = telebot.TeleBot(get_str_env('TOKEN'))
rater = Rater()

bot.send_message(
    get_int_env('ADMIN_ID'),
    'Бот запущен.',
)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup_reply = telebot.types.ReplyKeyboardMarkup(True)
    currencies = telebot.types.KeyboardButton('Посмотреть курсы валют')
    markup_reply.add(currencies)
    bot.send_message(
        message.chat.id,
        'Выберите действие:',
        reply_markup=markup_reply
    )
    logging.warning(f'Пользователь {message.chat.id} нажал кнопку start.')


@bot.message_handler(content_types=['text'])
def print_message(message):
    logging.warning(f'Пользователь {message.chat.id} ввел "{message.text}".')
    if message.text == 'Посмотреть курсы валют':
        currencies_to_rates: Dict[str, Dict[str, Union[str, float]]] = rater.currencies_data
        text: str = ''
        for currency, rate_emoji in currencies_to_rates.items():
            text = text + emojis.encode(f"{rate_emoji['emoji']} Курс {currency} {rate_emoji['rate']}\n")
        bot.send_message(
            message.chat.id,
            text
        )
    else:
        bot.send_message(
            message.chat.id,
            'Такого действия не существует! Выберите действие на клавиатуре!'
        )


bot.polling()
