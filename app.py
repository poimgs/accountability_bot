from flask import Flask, request 
import telegram 
from telebot.credentials import bot_token, bot_user_name, URL
import time
import datetime

TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

context_tracker = ''
conversation_step_tracker = 0
contexts = {
    'what_is_important': 
    {
        'conversation_steps': ['first_question', 'first_question_why', 'second_question', 'second_question_why', 'wait'],
        'conversation_steps_answers': {'first_question': 'What was important to you today?', 'first_question_why': 'Why?', 'second_question': 'On a scale of 1-10, how was your day?','second_question_why': 'Why?', 'wait': 'Thank you for your answers, I am looking forward to hearing more from you tomorrow!'}
    }
}

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

def conversation(chatId):
    global context_tracker
    global conversation_step_tracker
    global contexts

    max_steps = len(contexts[context_tracker]['conversation_steps_answers']) 

    if conversation_step_tracker < max_steps:
        # Also collect the latest message and store it somewhere 
        current_step = contexts[context_tracker]['conversation_steps'][conversation_step_tracker]
        message = contexts[context_tracker]['conversation_steps_answers'][current_step]

        bot.sendMessage(chat_id=chatId, text=message)
        conversation_step_tracker += 1
    else:
        current_step = contexts[context_tracker]['conversation_steps'][conversation_step_tracker]
        message = contexts[context_tracker]['conversation_steps_answers'][current_step]

        bot.sendMessage(chat_id=chatId, text=message)

        #restart 
        context_tracker = ''
        conversation_step_tracker = 0

        #Resend messages after a while
        wait(chat_id)

def first_conversation(chatId):
    global context_tracker
    global conversation_step_tracker
    global contexts

    bot.sendMessage(chat_id=chatId, text='Hello Steven! The Telegram bot is now working! :D')
    context_tracker = 'what_is_important'

    current_step = contexts[context_tracker]['conversation_steps'][conversation_step_tracker]
    message = contexts[context_tracker]['conversation_steps_answers'][current_step]

    bot.sendMessage(chat_id=chatId, text=message)
    conversation_step_tracker += 1

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
    if text == '/start':
        context_tracker = ''
        conversation_step_tracker = 0
        first_conversation(chat_id)
    elif context_tracker:
        conversation(chat_id)
    else:
        first_conversation(chat_id)
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