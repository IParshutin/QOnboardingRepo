import re
import telebot
from BotBody.auth_data import token
import mysql.connector
from transliterate import translit

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="admin",
    database="mydb"
)
mycursor = mydb.cursor()
mycursor.execute("SELECT  story FROM jokes ORDER BY rand() LIMIT 1;")
myresult = mycursor.fetchall()

for x in myresult:
    print(x)


def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Напиши слово Жопа и получишь анекдот!")

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        text = translit(message.text.lower(), 'ru')
        if findWholeWord('жопа')(text):
            try:
                # mycursor.execute('SELECT story FROM jokes ORDER BY rand() LIMIT 1;')
                mycursor.execute('SELECT  story FROM jokes ORDER BY rand() LIMIT 1;')
                myresult = mycursor.fetchall()
                bot.send_message(
                    message.chat.id, myresult)
            except Exception as ex:
                print(ex)
                bot.send_message(
                    message.chat.id,
                    "Damn...Something was wrong..."
                )

    bot.polling()


if __name__ == '__main__':
    # get_data()
    telegram_bot(token)
