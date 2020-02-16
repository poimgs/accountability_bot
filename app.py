from flask import Flask, request 
import telegram 
from telebot.credentials import bot_token, bot_user_name, URL
import time
import datetime

# Creating bot object and app object
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

# trackers to keep track of conversation
context_tracker = ''
conversation_step_tracker = 0

contexts = {
    'what_is_important': 
    {
        'conversation_steps': 
            ['What was important to you today?', 
             'Why?', 
             'On a scale of 1-10, how was your day?',
             'Why?', 
             'Thank you for your answers, I am looking forward to hearing more from you tomorrow!']
    }
}

# wait for a period of time before repeating questions in "what is important"
def wait(chatId):
    # get tomorrow's preferred date 
    bot.sendMessage(chat_id=chatId, text='You should receive a message in about 5 seconds')
    now = datetime.datetime.now()

    # wait a certain number of seconds
    test_time = now + datetime.timedelta(seconds=5)

    to_wait = test_time - now
    to_wait = to_wait.total_seconds()
    time.sleep(to_wait)

    bot.sendMessage(chat_id=chatId, text='Hello!')

# takes note of conversation trackers and provide appropriate responses 
def conversation(chatId):
    global context_tracker
    global conversation_step_tracker
    global contexts

    max_steps = len(contexts[context_tracker]['conversation_steps']) - 1

    if conversation_step_tracker < max_steps:
        # Also collect the latest message and store it somewhere 
        message = contexts[context_tracker]['conversation_steps'][conversation_step_tracker]

        bot.sendMessage(chat_id=chatId, text=message)
        conversation_step_tracker += 1
        print(conversation_step_tracker)
        print(context_tracker)
    else:
        message = contexts[context_tracker]['conversation_steps'][conversation_step_tracker]

        bot.sendMessage(chat_id=chatId, text=message)

        #restart 
        # context_tracker = ''
        conversation_step_tracker = 0
        print(conversation_step_tracker)
        print(context_tracker)
        #Resend messages after a while
        wait(chatId)

# if user is talking to bot for the first time, initiate first conversation
def first_conversation(chatId):
    global context_tracker
    global conversation_step_tracker
    global contexts

    bot.sendMessage(chat_id=chatId, text='Hello Steven! The Telegram bot is now working! :D')
    context_tracker = 'what_is_important'
    message = contexts[context_tracker]['conversation_steps'][conversation_step_tracker]

    bot.sendMessage(chat_id=chatId, text=message)
    conversation_step_tracker += 1

# receives telegram updates whenever a user sends a message
@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    global context_tracker
    global conversation_step_tracker
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
        context_tracker = ''
        conversation_step_tracker = 0
        first_conversation(chat_id)
    else:
        conversation(chat_id)
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