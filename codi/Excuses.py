#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import os
from telebot import types
#/setinline frase
#/setinlinefeedback enable

TOKEN = '564856484:AAHFDT6nmEjfz4JkIPS1DzY_V9gq-Cfl6Ec' 
bot = telebot.TeleBot(TOKEN)

excuses={
	"tard":["El tren va en retras","No he canviat l'hora","El mobil no m'ha despertat","No sabia que la classe començava a les 8"],
	"practica fora temps":["Windows no funciona","El gos s'ha menjat l'arxiu","Ah! He oblidat annexar l'arxiu","No tens el document compartit?","Tinc la feina feta, però està a casa.","He fet tard perquè en ma casa fa molt de fred i el cola cao no es dissolia amb la llet.",
	"No he pogut lliurar el treball perquè han entrat a robar a ma casa i s'han emportat el meu ordinador"],
	"classe":["No estava copiant, estava mirant si el meu company ho ha fet bé.","No és que no estigui fent res, s'està descarregant un programa.","No faig la feina perquè a mi m'agrada fer els deures a casa.","He faltat a classe per temes personals, a partir de demà ja no arribaré tard i vindré tots els dies."]
}

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
    	results=cercarExcusa(inline_query.query)
   	)

def cercarExcusa(consulta):
	resultats=[]
	i=0
	for motiu in excuses.keys():
		if motiu.find(consulta) != -1:
			for exc in excuses[motiu]:
				i+=1
				resultats.append(
            		types.InlineQueryResultArticle(
             		i,
                	exc,
                	types.InputTextMessageContent(exc)
            		)
        	) 		
	return resultats
			
bot.polling()
#https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/inline_example.py
