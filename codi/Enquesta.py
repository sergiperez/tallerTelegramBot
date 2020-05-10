#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import telebot
from telebot import types

TOKEN = '713706783:AAHBNVOYWME0sgYzb1n04aMv4NECnEol8Co' 
bot = telebot.TeleBot(TOKEN) 
adminUser= "sergipd" # chatID que 
opcions=[]
enquesta=""
text=""
respostes={}
vots={}

def admin(missatge):
	global adminUser
	return ((missatge.from_user.username==adminUser) and (missatge.chat.type == "private"))

@bot.message_handler(commands=['reset'])
def reset(missatge):
	if (admin(missatge)):
		respostes={}
		vots={}
		enquesta=""
		opcions=[]
	else:
		bot.send_message(missatge.chat.id,"No ets l'administrador")

@bot.message_handler(commands=['respondre'])
def respondre(missatge):
	if (len(enquesta)>0):		
		if (missatge.from_user.username not in respostes.keys()):
			markup = types.ReplyKeyboardMarkup(row_width=1)
			for opcio in opcions:
				markup.add(types.KeyboardButton(opcio))
			resposta=bot.send_message(missatge.chat.id,enquesta,reply_markup=markup)
			bot.register_next_step_handler(resposta, guardarResposta)
		else:
		    bot.send_message(missatge.chat.id,"Ja has respost l'enquesta")		
	else:
		bot.send_message(missatge.chat.id,"No hi ha enquesta")

def guardarResposta(resposta):
	respostes[resposta.from_user.username]=resposta.text
	vots[resposta.text]=vots[resposta.text]+1
	bot.send_message(resposta.chat.id,"Gràcies per respondre l'enquesta")	
	

@bot.message_handler(commands=['resultats'])
def resultats(missatge):
	for vot in vots.keys():
	    bot.send_message(missatge.chat.id,str(vot)+"--"+str(vots[vot]))		
    
@bot.message_handler(commands=['qui'])
def qui(missatge):
	for q in respostes.keys():
	    bot.send_message(missatge.chat.id,q)		

@bot.message_handler(commands=['start'])
def inici(missatge):
	if (admin(missatge)):
		bot.send_message(missatge.chat.id,"Benvingut administrador, escriu l'enquesta")
	else:
		bot.send_message(missatge.chat.id,"Amb l'opció /respondre pots votar a l'enquesta, /resultats per veure com van els vots i /qui per saber qui ha votat")

#Escoltar missatges per crear Enquesta
def listener(missatges):
	for missatge in missatges:
		if (admin(missatge) and missatge.text != "Titol enquesta" and missatge.text!="Opcions" and missatge.text[0]!="/"):
			global text
			text=missatge.text
			markup = types.ReplyKeyboardMarkup()
			markup.add(types.KeyboardButton("Titol enquesta"),types.KeyboardButton("Opcions"))
			resposta=bot.send_message(missatge.chat.id,"Què és titol o opcions?",reply_markup=markup)
			bot.register_next_step_handler(resposta, crearEnquesta)

def crearEnquesta(resposta):
	global enquesta
	global text
	if (resposta.text=="Titol enquesta"):
		enquesta=text
		bot.send_message(resposta.chat.id,"Titol creat, gràcies!")
	elif (resposta.text=="Opcions"):
		opcions.append(text)
		vots[text]=0
		bot.send_message(resposta.chat.id,"Opció afegida")				
		

bot.set_update_listener(listener) 		
bot.polling() 
