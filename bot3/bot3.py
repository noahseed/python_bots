# -- coding: utf-8 --
import requests
import telebot
from telebot import types
import pymysql

conn = pymysql.connect(host='127.0.0.1',
                       unix_socket='/opt/lampp/var/mysql/mysql.sock',
                       user='root',
                       passwd=None,
                       db='users_telegram')

cur = conn.cursor()

API_TOKEN = '5752517622:AAEOxnc1mWg0IcNSo9V0b6CXkKuFc12zzo4'

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}

class User:
    def __init__(self,name):
        self.name = name
        self.age = None
        self.team = None
        self.mail = None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    msg = bot.reply_to(message,"Hellow !\nCe bot est un bot de test.")
    cid = message.chat.id
    bot.send_message(cid, "Notre ID est: " + str(cid) + "\nQuel est votre prénom ?")
    bot.register_next_step_handler(msg, process_firstname_step)


def process_firstname_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, "Quel age avez-vous ?")
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, e)


def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, "Vous devez entrer un numéro!\nQuel age avez-vous ?")
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Gremio', 'Internacional')
        msg = bot.reply_to(message, "Quelle est votre équipe de coeur ?", reply_markup=markup)
        bot.register_next_step_handler(msg, process_team_step)
    except Exception as e:
        bot.reply_to(message, 'Oups, une erreur est survenue')
        print(e)


def process_team_step(message):
    try:
        chat_id = message.chat.id
        team = message.text
        user = user_dict[chat_id]
        if (team == u'Gremio') or (team == u'Internacional'):
            user.team = team
        else:
            raise Exception()
        msg = bot.reply_to(message, 'Quelle est votre adresse email ?')
        bot.register_next_step_handler(msg, process_mail_step)
    except Exception as e:
        bot.reply_to(message,e)


def process_mail_step(message):
    try:
        chat_id = message.chat.id
        mail = message.text
        user = user_dict[chat_id]
        cur.execute('USE users_telegram')
        sql = "INSERT INTO user (`user_name`, `user_chatid`, `user_category`, `user_email`, `user_age`) VALUES (%s,%s,%s,%s,%s)"
        val = (user.name,str(chat_id),user.team,mail,str(user.age))
        cur.execute(sql,val)
        conn.commit()
        cur.close()
        conn.close()
        msg = bot.reply_to(message, "Merci de vous être enregistré")
    except Exception as e:
        bot.reply_to(message,e)


bot.enable_save_next_step_handlers(delay=5)
bot.load_next_step_handlers()

bot.polling()
