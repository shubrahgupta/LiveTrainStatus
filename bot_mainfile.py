import os
import requests
import telebot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')



def get_status(train: int) -> dict:
    """Get train running status.
    Keyword arguments:
    train:str - Train Number
    Return:dict - JSON data with the origin, and status of the train
    """
    url = os.environ.get('URL') #website of flask server running the RestAPI for scraping the source website
    url += "/" + str(train)
    response = requests.get(url)
    return response.json()




bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "How you doing?")


@bot.message_handler(commands=['train'])
def sign_handler(message):
    text = "Enter the train number"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, fetch_train_status)


def fetch_train_status(message):
    train_num = message.text
    data = get_status(train_num)

    output_message = f'*For the train:* {data["train"]}\n*Origin:* {data["origin"]}\n*Status:* {data["status"]}'

    bot.send_message(message.chat.id, output_message, parse_mode="Markdown")




@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()