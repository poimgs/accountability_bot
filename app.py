from flask import Flask, request 
import telegram 
from telebot.credentials import bot_token, bot_user_name, URL

TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    # for debugging purposes only
    print("got text message :", text)
    # the first time you chat with the bot AKA the welcoming message
    one_to_ten = ['1', '2', '3', '4', '5', '6', '7', '8', '9' ,'10']
    if text == "/start":
        # print the welcoming message
        bot_welcome = 'Hello Steven! The Telegram bot is now working! :D'
        first_question = 'On a scale of 1-10, how was today?'
        # send the welcoming message
        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
        bot.sendMessage(chat_id=chat_id, text=first_question, reply_to_message_id=msg_id)
    elif text in one_to_ten:
        second_question = 'Why?'
        bot.sendMessage(chat_id=chat_id, text=second_question, reply_to_message_id=msg_id)
    else:
        bot.sendMessage(chat_id=chat_id, text='Hello!', reply_to_message_id=msg_id)

    return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    app.run(threaded=True)
