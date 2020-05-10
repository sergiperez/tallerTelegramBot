#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import os
from telebot import types
#/setinline frase
#/setinlinefeedback enable
#Activar obrint conversa

TOKEN = '593123776:AAEoDCUu34GGFHcL7HJHLoSv8MHqfCPIHwI' 
bot = telebot.TeleBot(TOKEN)

acudits=[
"Crec que estas obsesionat amb el futbol i em fas falta.  Falta! Si no t'he tocat.",
"Cuantas anclas tiene un barco? 11 Por que? Porque siempre dicen 'eleven anclas'.",
"Per que als elefants no els agrada la informatica? Tenen por als ratolins.",
"Que desayuna Thor? Thor-tilla.",
"Que son 8 bocabits? Un bocabyte.",
"Que es un terapeuta?  Mil gigapeutas.",
"A l'escola els companys em diuen Facebook? I tu que els dius?  M'agrada.",
"Tens Wi-fi? Si I quina es la clau? Tenir diners i pagar-lo.",
"Com li diuen al cosi vegetaria de Bruce Lee? Broco Lee",
"Cual es el alimento mas filosofico? El pienso",
"Siempre que cuento este chiste los perros dicen: GUAU!",
"Donde pondrias un musico a jugar en un partido de futbol? En cualquiera de las bandas.",
"En una convencion de circos un hombre pregunta: Disculpe, donde estan las hermanas siamesas? En la Sala de Juntas."
]

@bot.inline_handler(lambda query: len(query.query) is 0)
def default_query(inline_query):
    bot.answer_inline_query(
    	inline_query.id,
    	results=[]
   	)

@bot.inline_handler(func=lambda query: True)
def query_text(inline_query):
   	bot.answer_inline_query(
    	inline_query.id,
    	results=cercarAcudit(inline_query.query)
   	)

def cercarAcudit(consulta):
	resultats=[]
	i=0
	for xist in acudits:
		if xist.upper().find(consulta.upper()) != -1:
			i+=1
			resultats.append(
            	types.InlineQueryResultArticle(
             	  i,
                xist,
                types.InputTextMessageContent(xist)
            	)
        	) 		
	return resultats
			
bot.polling()
#https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/inline_example.py
