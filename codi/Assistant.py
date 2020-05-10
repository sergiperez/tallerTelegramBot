# -*- coding: utf-8 -*-
import requests
import telebot
import os
from telebot import types

TOKEN = '727677165:AAF7uXW3DcV-vkmGkvS4lIdJ5fxU7m6XBCg' 
bot = telebot.TeleBot(TOKEN)	


### Comandes del bot ####
##https://www.pythonforbeginners.com/os/pythons-os-module
@bot.message_handler(commands=['file'])
def list_command(missatge):
    if (missatge.from_user.username == "sergipd"):
      files = os.listdir(os.getcwd())
      text="Quin fitxer vols?\n"
      markup = types.ReplyKeyboardMarkup()
      for f in range(0,len(files)):
          markup.add(types.KeyboardButton(files[f])) 
      answer=bot.send_message(missatge.chat.id,text,reply_markup=markup)
      bot.register_next_step_handler(answer, download)
    else:
      bot.send_message(missatge.chat.id,"No tens permisos")

def download(missatge):
	doc = open(os.getcwd()+"/"+missatge.text, 'rb')
	bot.send_document(missatge.chat.id, doc)       


@bot.message_handler(commands=['start'])
def start_command(missatge):
   bot.send_message(
       missatge.chat.id,
       "T'has deixat les pràctiques a casa? Jo te la puc trobar. Escriu la comanda file\n "
   )    

bot.polling()
