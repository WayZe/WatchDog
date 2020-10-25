import emojis
import telebot
import logging
from parser import Rater
from typing import Dict, Union, List
from postgres_storage import PostgresStorage
from functions import get_str_env, get_int_env


rater = Rater()
postgres_storage = PostgresStorage()
bot = telebot.TeleBot(get_str_env('TOKEN'))

bot.send_message(
    get_int_env('ADMIN_ID'),
    'Бот запущен.',
)

diffs_to_emojis = {
    'up': ':arrow_up:',
    'down': ':arrow_down:'
}


@bot.message_handler(commands=['start'])
def start_message(message):

    def get_greeting(chat):
        name_parts: List[str] = []

        first_name: Optional[str] = chat.first_name
        if first_name is not None:
            name_parts.append(first_name)

        last_name: Optional[str] = chat.last_name
        if last_name is not None:
            name_parts.append(last_name)

        return ' '.join(name_parts)

    markup_reply = telebot.types.ReplyKeyboardMarkup(True)
    currencies = telebot.types.KeyboardButton('Курсы валют')
    markup_reply.add(currencies)
    greeting: str = get_greeting(message.chat)
    bot.send_message(
        message.chat.id,
        f'Привет, {greeting}!\n'
        'Выберите, что вы хотите посмотреть.',
        reply_markup=markup_reply
    )
    postgres_storage.add_user(message.chat.id)
    logging.warning(f'Пользователь {message.chat.id} нажал кнопку start.')


@bot.message_handler(content_types=['text'])
def print_message(message):
    logging.warning(f'Пользователь {message.chat.id} ввел "{message.text}".')
    if message.text == 'Курсы валют':
        currencies_to_rates: Dict[str, Dict[str, Union[str, float]]] = rater.currencies_data
        text: str = ''
        for currency, value in currencies_to_rates.items():
            diff: str = diffs_to_emojis['up'] if value['diff'] > 0 else diffs_to_emojis['down']
            text = text + emojis.encode(f"{value['emoji']} Курс {currency} {value['rate']} {diff}\n")
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
