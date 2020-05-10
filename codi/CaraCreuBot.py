# -*- coding: utf-8 -*-
import telebot
import random
from telebot import types

TOKEN = '521615312:AAG9iFeXt9QZmnHq37mDa9nFSja4HWYPKd4' 
bot = telebot.TeleBot(TOKEN)
ranking={}	


### Comandos del bot ####
@bot.message_handler(commands=['tirar'])
def tirar_command(missatge):
	markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
	markup.add(types.KeyboardButton("Cara"),types.KeyboardButton("Creu"))
	resposta=bot.send_message(missatge.chat.id,"Hola  que vols apostar cara o creu?",reply_markup=markup)
	bot.register_next_step_handler(resposta, jugar)

def jugar(missatge):
	moneda=random.randrange(2)
	bot.send_message(missatge.chat.id,"Ha sortit ...")
	photo = open(str(moneda)+'.png', 'rb')
	bot.send_photo(missatge.chat.id, photo)
	if ((moneda==0 and missatge.text=="Cara") or (moneda==1 and missatge.text=="Creu")):
		bot.send_message(missatge.chat.id,"Has guanyat")
		audio = open('aplaudiments.mp3', 'rb')
		bot.send_audio(missatge.chat.id, audio) 
		ranking[missatge.from_user.username][0]+=1
	else:
		bot.send_message(missatge.chat.id,"Has perdut")	
		ranking[missatge.from_user.username][1]+=1

# filter on a specific message
@bot.message_handler(func=lambda message: message.text == "Cara")
def command_cara(m):
    jugar(m)
    # default handler for every other text
@bot.message_handler(func=lambda message: message.text == "Creu")
def command_creu(m):
    jugar(m)

@bot.message_handler(commands=['rank'])	
def rank(missatge):
	for user in ranking:
		victories=float(ranking[user][0])
		derrotes=float(ranking[user][1])
		if ((victories+derrotes)==0):
			bot.send_message(missatge.chat.id,str(user)+" encara no has jugat cap partida")
		else:	
			bot.send_message(missatge.chat.id,str(user)+" ha guanyat "+str(victories/float(victories+derrotes)*100)+"%")


@bot.message_handler(commands=['start'])
def start_command(missatge):
   bot.send_message(
       missatge.chat.id,
       'Gràcies per voler jugar al cara i creu.\n' +
       'Per jugar executa la comanda /tirar.\n' +
       'Per veure el ranking /rank.'
   )    
   ranking[missatge.from_user.username]=[0,0]

bot.polling()

#Inlinehandler
#grups
#saber que és el lamba