import telegram 
from telebot.credentials import bot_token, bot_user_name, URL
import datetime
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

def keep_accountable():
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = connection.cursor()

    get_history_query = "SELECT * FROM accountability ORDER BY id DESC LIMIT 1"
    cursor.execute(get_history_query)
    rows = cursor.fetchall()

    connection.commit()
    connection.close()

    last_timestamp = rows[0][1]
    last_timestamp = datetime.datetime.strptime(last_timestamp,"%Y-%m-%d %H:%M:%S")
    last_timestamp_modified = datetime.datetime(last_timestamp.year,last_timestamp.month,last_timestamp.day,last_timestamp.hour)

    now = datetime.datetime.now()
    now_modified = datetime.datetime(now.year,now.month,now.day,now.hour)
    one_hour_before = now_modified - datetime.timedelta(hours=1)

    one_day_before = now_modified - datetime.timedelta(days=1)

    print(last_timestamp_modified)
    print(one_hour_before)
    print(one_day_before)

    if last_timestamp_modified == one_hour_before:
        bot.sendMessage(chat_id=247547763, text='What is your current choice?')
    
    elif last_timestamp_modified == one_day_before:
        bot.sendMessage(chat_id=247547763, text='Hey, it\'s been a day since you last updated me, seems like you are crashing or have crashed')
        bot.sendMessage(chat_id=247547763, text='It\'s time to seek help! :)')

if __name__ == '__main__':
    keep_accountable()

# hopefully github is integrated with heroku!