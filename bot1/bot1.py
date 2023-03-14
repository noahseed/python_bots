#-- coding: utf-8 --
import telebot
from telebot import types

API_TOKEN = '5752517622:AAEOxnc1mWg0IcNSo9V0b6CXkKuFc12zzo4'

bot = telebot.TeleBot(API_TOKEN)

# Commande /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
	cid = message.chat.id
	msg = bot.reply_to(message, "Hellow!\nNotre id est: " + str(cid))
	bot.send_message(cid, "Si vous avez besoin d'aide, utilisez la fonction /help")


# Commande /help
@bot.message_handler(commands=['help'])
def send_help(message):
	cid = message.chat.id
	msg_help = bot.reply_to(message, "Options disponibles:\nOption 1: /enregistrer\nOption 2: /categories\nOption 3: /contact")
	bot.send_message(cid, "Si vous rencontrez des difficultés, envoyez un message à sebastien@rondeau-cameira.fr")


# Commande /categories
@bot.message_handler(commands=['categories'])
def send_categories(message):
	cid = message.chat.id
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
	markup.add('Chaussures', 'Vêtements')
	msg_cat = bot.reply_to(message, "Choisissez la catégorie souhaitée:", reply_markup=markup)

bot.polling()