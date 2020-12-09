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

    markup_reply = telebot.types.ReplyKeyboardMarkup(True)
    settings = telebot.types.KeyboardButton('Настройки')

    markup_reply.add(currencies, settings)

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

        bot.send_message(
            message.chat.id,
            rater.formatted_currencies()
        )

    elif (message.text == 'Настройки' or
          message.text == 'Уведомления включены' or
          message.text == 'Уведомления отключены'):

        user_id: int = message.chat.id
        if message.text == 'Настройки':
            notification_state = postgres_storage.get_notification_state_for_user(user_id)
            notification_button = 'включены' if notification_state else 'отключены'
        elif message.text == 'Уведомления включены':
            notification_button = 'отключены'
            postgres_storage.set_notification_for_user(user_id, False)
            bot.send_message(
                message.chat.id,
                'Вы отключили уведомления'
            )
        elif message.text == 'Уведомления отключены':
            notification_button = 'включены'
            postgres_storage.set_notification_for_user(user_id, True)
            bot.send_message(
                message.chat.id,
                'Вы включили уведомления'
            )

        markup_reply = telebot.types.ReplyKeyboardMarkup(True)
        frequency = telebot.types.KeyboardButton(f'Уведомления {notification_button}')

        markup_reply = telebot.types.ReplyKeyboardMarkup(True)
        back = telebot.types.KeyboardButton('В начало')

        markup_reply.add(frequency, back)

        bot.send_message(
            message.chat.id,
            f'Выберите пункт настроек:',
            reply_markup=markup_reply
        )

    elif message.text == 'В начало':

        markup_reply = telebot.types.ReplyKeyboardMarkup(True)
        currencies = telebot.types.KeyboardButton('Курсы валют')

        markup_reply = telebot.types.ReplyKeyboardMarkup(True)
        settings = telebot.types.KeyboardButton('Настройки')
        markup_reply.add(currencies, settings)

        bot.send_message(
            message.chat.id,
            'Выберите, что вы хотите посмотреть.',
            reply_markup=markup_reply
        )

    else:
        bot.send_message(
            message.chat.id,
            'Такого действия не существует! Выберите действие на клавиатуре!'
        )


bot.polling()
