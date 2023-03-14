#-- coding: utf-8 --
import telebot
import json
import urllib.request

API_TOKEN = '5752517622:AAEOxnc1mWg0IcNSo9V0b6CXkKuFc12zzo4'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['cep'])

def send_cep(message):
	msg = bot.reply_to(message, """tapez le cep souhaité:""")
	cid = message.chat.id
	bot.register_next_step_handler(msg, send_cep_step)


def send_cep_step(message):
	cid = message.chat.id
	msg_cep = message.text
	url = "https://viacep.com.br/ws/" + msg_cep + "/json/"
	response = urllib.request.urlopen(url)

	data = json.loads(response.read())

	print(data)

	cep = data['cep']
	logradouro = data['logradouro']
	bairro = data['bairro']
	localidade = data['localidade']
	uf = data['uf']
	bot.send_message(cid, "CEP: " + cep + "\nLogradouro: " + logradouro + "\nBairro: " + bairro + "\nLocalidade: " + localidade + "\nUF: " + uf)


bot.polling()