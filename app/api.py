import telebot
from functions import get_str_env
from dotenv import load_dotenv
from parser import Rater

# нужно для локального запуска
load_dotenv()
bot = telebot.TeleBot(get_str_env('TOKEN'))


@bot.message_handler(commands=['start'])
def start_message(message):
    usd_rate: float = Rater.get_usd_rate()
    bot.send_message(message.chat.id, f'Курс доллара {usd_rate}')


bot.polling()
