from flask import Flask, request 
import telegram 
from telebot.credentials import bot_token, bot_user_name, URL
import time
import datetime
import sqlite3

# Creating bot object and app object
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

# wait for a period of time before repeating questions in "what is important"
def wait(chatId):
    # get tomorrow's preferred date 
    bot.sendMessage(chat_id=chatId, text='You should receive a message in about 5 minutes')
    now = datetime.datetime.now()

    # wait a certain number of seconds
    test_time = now + datetime.timedelta(minutes=5)

    to_wait = test_time - now
    to_wait = to_wait.total_seconds()
    time.sleep(to_wait)

    bot.sendMessage(chat_id=chatId, text='Hey Steven! What is your current focus?')

def save_message(message):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection = sqlite3.connect('data.db')

    cursor = connection.cursor()

    get_data_query = "SELECT * FROM accountability"
    result = cursor.execute(get_data_query)
    rows = result.fetchall()
    last_index = rows[-1][0]

    index_to_insert = last_index + 1

    row_to_insert = (index_to_insert, current_time, message)
    insert_query = "INSERT INTO accountability values (?,?,?)"
    cursor.execute(insert_query, row_to_insert)

    connection.commit()

    connection.close()

# receives telegram updates whenever a user sends a message
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

    # simple logic flow 
    if text == '/start':
        bot.sendMessage(chat_id=chat_id, text='Yo Steven! This bot is up and running! :)')
    else:
        # Database logic here
        save_message(text)
        bot.sendMessage(chat_id=chatId, text='Thanks for keeping me updated! :D')
        wait()
    return 'ok'

# To set webhook for telegram to send POST requests to 
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