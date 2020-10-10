import emojis
import telebot
from functions import get_str_env
from dotenv import load_dotenv
from parser import Rater

# нужно для локального запуска
load_dotenv()

bot = telebot.TeleBot(get_str_env('TOKEN'))


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        r'Введите /currencies для получения курса валют.'
    )


@bot.message_handler(commands=['currencies'])
def currency_message(message):
    rater = Rater()
    currencies_to_rates: float = rater.get_all()
    for currency, rate_emoji in currencies_to_rates.items():
        bot.send_message(
            message.chat.id,
            emojis.encode(f"{rate_emoji['emoji']} Курс {currency} {rate_emoji['rate']}")
        )


bot.polling()
