import telegram 
from telebot.credentials import bot_token, bot_user_name, URL


def start():
    TOKEN = bot_token
    bot = telegram.Bot(token=TOKEN)

    chat_id = 247547763
    bot.sendMessage(chat_id=chat_id, text='What is your current focus?')

if __name__ == '__main__':
    start()