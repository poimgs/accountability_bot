import telegram 
from telebot.credentials import bot_token, bot_user_name, URL


def start():
    TOKEN = bot_token
    bot = telegram.Bot(token=TOKEN)

    chat_id = ''
    bot.sendMessage(chat_id=chat_id, text='Ok! Your history of messages has been deleted!')

if __name__ == '__main__':
    start()