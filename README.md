# El meu primer TelegramBot

## Índex sessió:

1. Objectiu taller.
2. Configurar entorn
3. Explicació de què és un Bot. Tipus de bots.
4. API TelegramBotApi
5. Programar primer Bot: bot conversa 1 a 1
5.1. Creació bot a @BotFather i configuració essencial.
5.2. Bot per enviar arxius.
5.3. Bot per jugar al cara i creu.
6. Programar segon Bot: inline. Generar acudits o excuses.
7. Programar tercer Bot: afegir a un grup.
8. Referències

## 2. Configurar entorn

Per poder programar correctament un Bot s'ha de:
Tenir coneixement bàsics de Python (perquè és el llenguatge en què s'escull l'API)
Tenir usuari del Telegram.
Recomanable: activar la versió web del Telegram.  Obriu al navegador la web: [http://web.telegram.org](http://web.telegram.org) . Us envia un codi d'activació.

![](https://i.imgur.com/2KWqkKp.png)


Instal·lar l'API al vostre ordinador:

```bash=
sudo apt install python3-pip
sudo pip3 install pyTelegramBotAPI
```

![](https://i.imgur.com/OMkm65x.png)


## 3 Tipus de bot

Farem tres tipus de Bot:
### 3.1 Bots de conversa un a un: 
- Aquells on l'usuari obrirà una conversa privada amb el Bot.
- Poden ser jocs, enviar-nos informació...

Exemple @triviaBot.

### 3.2.  Bots inline:
S'usen des de la línia d'escriptura de missatge.
Aquells que ens ajuden quan estem conversant amb algú, ens ajuden a crear missatges o enviar imatges.
Exemple @Gif @Youtube.

![](https://i.imgur.com/KJb212I.png)

### 3.3. Bots en un grup:

S'afegeixen com un membre més d'un grup i responen quan se'ls passa una comanda (inicia per /)
Poden ser per fer enquestes en un grup, presa de decisions, jocs...etc.
Exemple @vot

## 4. API

L'API ens dóna una sèrie de funcions que ens permet interactuar amb la plataforma de Telegram.

Telegram és codi obert i permet accedir als seus continguts i funcionalitats via crides HTTP. 
La API fet amb Python ens facilita l'accés i ens encapsula les crides HTTP i els tractaments dels seus resultats que estan codificats en JSON.

L'API escollida és pyTelegramBotApi que és codi obert.
Per lligar el codi del nostre Bot amb el Telegram l'API usa un TOKEN (identificador) que dóna Telegram per a cada Bot creat.


Per treballar en el taller usarem el grup de Telegram [https://t.me/joinchat/C410CQ-UzEwM5hZFxlx_bQ](https://t.me/joinchat/C410CQ-UzEwM5hZFxlx_bQ)
 
## 5. Primer BOT: Conversa un a un

### 5.1. BotFather

Creació del bot a Telegram per això s'usa un Bot !!! Ole ole! El Bot és el @BotFather. 

![](https://i.imgur.com/0nSuOn0.png)

Obriu conversa amb el BotFather.
Té una sèrie de comandes. Useu la comanda /newbot.

Poseu en el següent missatge el nom del Bot: CaraCreu$VOSTRENOM$ o Fitxer$VOSTRENOM$
Després poseu el nom del Bot (serà el @), poseu al mateix però al final Bot. CaraCreu$VOSTRENOM$Bot o Fitxer$VOSTRENOM$Bot.

Podem posar més característiques del Bot . Interessa /setcommands per posar les comandes. **Però som programadors i ho farem per CODI!**
 
### 5.2. Bot que recupera arxiu del nostre PC

Primer hem de lligar el programa Python amb l'API de telegram.

Orbiu un nou arxiu de Python de nom fitxerBot.py i escriviu:

```python3=
import os
import telebot
from telebot import types

TOKEN = 'TOKEN DONAT PER @BOTFATHER'
#L'objecte bot interactuarà amb l'API
bot = telebot.TeleBot(TOKEN)
``` 

I ara el que hem de fer es respondre al start. Per tant hem de definir que li direm a l'usuari  quan obri conversa amb el nostre bot.

Abans de la funció que tractarà la comanda es posa:
@bot.message_handler(commands=['start'])
def start_command(missatge):

Al definir la funció hem de tenir en compte que reben un objecte missatge del que ens interessa:
**missatge.chat.id** Identificador únic del xat
**missatge.from_user**  Objecte del usuari. 
**missatge.from_user.username**

L'objecte bot té diverses funcions una és:
**bot.send_message(chat_id, text)**

Quan acabem perquè el bot es quedi pendent a l'espera de missatges s'executa la funció **bot.polling()**.

Veieu aquí el primer codi: (també afegim llibreria os per treballar amb el disc real)

```python3=
import os
import telebot
from telebot import types

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_command(missatge):
   bot.send_message(
   	missatge.chat.id,
   	"Per recuperar un fitxer de l'ordinador de casa usa la comanda /file"
   )    

bot.polling()
```

Executeu python i el nom del vostre fitxer al terminal. 

Obriu conversa amb el bot, hem tingut èxit?

Ara anem a fer l'acció de recuperar el fitxer.
Usarem l'objecte markup perquè ens mostri els fitxer com llista de botons.

```python3=
@bot.message_handler(commands=['file'])
def file_command(missatge):
    files = os.listdir(os.getcwd())
    markup = types.ReplyKeyboardMarkup()
    for f in range(0,len(files)):
      markup.add(types.KeyboardButton(files[f]))
    answer=bot.send_message(missatge.chat.id,"Quin fitxer vols?\n",reply_markup=markup)
    bot.register_next_step_handler(answer, download)
```

Es mostra aquest menú resposta a l'usuari amb la funció send_message com abans però un tercer argument que és el menú de teclat creat abans.
Després es recull que ha dit l'usuari i s'envia el programa a la funció que decideix si guanya o no. Amb la funció  bot.register_next_step_handler(resposta, nomseguentfuncio)


```python3=
resposta=bot.send_message(missatge.chat.id,"Quin fitxer vols?\n",reply_markup=markup)
    bot.register_next_step_handler(resposta, download)
```

El codi de la funció quedaria:
```python3=
def download(missatge):
    doc = open(os.getcwd()+"/"+missatge.text, 'rb')
    bot.send_document(missatge.chat.id, doc) 
```

Millora: 

**Qui pot accedir al nostre ordinador ara? Amb la propietat missatge.from_user.username podem saber el nom de l'usuari.**

###  5.3. Joc de cara i creu

Primer lligar el programa Python amb l'API de telegram.

```python3=
import telebot
from telebot import types

TOKEN = 'TOKEN DONAT PER @BOTFATHER'
#L'objecte bot interactuarà amb l'API
bot = telebot.TeleBot(TOKEN)
```

I ara el que hem de fer es respondre al start. Per tant hem de definir que li direm a l'usuari  quan obri conversa amb el nostre bot.

Abans de la funció que tractarà la comanda es posa:
@bot.message_handler(commands=['start'])
def start_command(missatge):

Al definir la funció hem de tenir en compte que reben un objecte missatge del que ens interessa:
**missatge.chat.id** Identificador únic del xat
**missatge.from_user**  Objecte del usuari. 
**missatge.from_user.username**

L'objecte bot té diverses funcions una és:
**bot.send_message(chat_id, text)**
Quan acabem perquè el bot es quedi pendent a l'espera de missatges s'executa la funció **bot.polling()**.

Veieu aquí el primer codi:

```python3=
import telebot
from telebot import types

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_command(missatge):
   bot.send_message(
   	missatge.chat.id,
   	'Amb /tirar poden jugar i /rank veure el ranking'
   )    
   ranking[missatge.from_user.username]=[0,0]

bot.polling()
```

Executeu python i el nom del vostre fitxer al terminal. 

Obriu conversa amb el bot, hem tingut èxit?
Ara anem a fer l'acció de jugar d'apostar.

Com ho feu?
Primer se li mostra a l'usuari què vol apostar. Es fa amb la classe **types.ReplyKeyboardMarkup**.

```python3=
@bot.message_handler(commands=['tirar'])
def tirar_command(missatge):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    markup.add(types.KeyboardButton("Cara"),types.KeyboardButton("Creu"))
```

Es mostra aquest menú resposta a l'usuari amb la funció send_message com abans però un tercer argument que és el menu de teclat creat abans.

Després es recull que ha dit l'usuari i s'envia el programa a la funció que decideix si guanya o no. Amb la funció  bot.register_next_step_handler(resposta, nomseguentfuncio).

resposta=bot.send_message(missatge.chat.id,"Hola  que vols apostar cara o creu?",reply_markup=markup)
    bot.register_next_step_handler(resposta, decisio)

El codi de la funció quedaria:

```python3=
@bot.message_handler(commands=['tirar'])
def tirar_command(missatge):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    markup.add(types.KeyboardButton("Cara"),types.KeyboardButton("Creu"))
    resposta=bot.send_message(missatge.chat.id,"Hola  que vols apostar cara o creu?",reply_markup=markup)
    bot.register_next_step_handler(resposta,decisio)
```

La funció que decideix (funció normal de Python) ha de:
- Llençar una moneda. Com ho feu? Random?
- Si l'usuari guanya enviar un missatge dient guanyat i sinó derrota.
- Si la moneda és 0 i el resposta.text és Cara guanya.
- Si la moneda és 1 i el resposta.text és Creu guanya.
- Sinó perd.

Millores podeu posar just després de generar el random, enviar una imatge de la moneda si és cara o creu.

```python3=
def decisio(missatge):
    #moneda és el resultat del random
    moneda=random.randrange(2)
    if ((moneda==0 and missatge.text=="Cara") or (moneda==1 and missatge.text=="Creu")):
   	 bot.send_message(missatge.chat.id,"Has guanyat")
    else:
   	 bot.send_message(missatge.chat.id,"Has perdut") 
```
     
Per enviar una imatge es fa amb:

```python3=
photo = open(str(moneda)+'.png', 'rb')
bot.send_photo(missatge.chat.id, photo)
```

Les imatges de les monedes les podeu aconseguir a la carpeta imatges.

## 6. Segon BOT: Inline (generador d'acudits o excuses)

Creeu un bot igual que abans però li direm Excuses$VOSTRENOM$
Però ara s'ha d'executar dues comandes més:
/setinline i us demanar frase a indicar que ha d'escriure usuari
/setinlinefeedback i seleccioneu enable.
Un cop el feu, el lligueu igual que abans.

```python3=
import telebot
import os
from telebot import types
#/setinline frase
#/setinlinefeedback enable

TOKEN = '564856484:AAHFDT6nmEjfz4JkIPS1DzY_V9gq-Cfl6Ec'
#Bot Father us ha donat aquest valor
bot = telebot.TeleBot(TOKEN)
```

Ara però com respon des de la línia d'escriptura de missatges heu d'implementar els següents mètodes (ja que no tenen comandes)
**@bot.inline_handler(lambda query: len(query.query) is 0)**
**@bot.inline_handler(func=lambda query: True)**

El primer és perquè no s'executi si usuari no escriu cap paraula i no fem res. 

```python3=
@bot.inline_handler(lambda query: len(query.query) is 0)
def default_query(inline_query):
	bot.answer_inline_query(
   	 inline_query.id,
   	 results=[]
  	 )
```

Ara la funció que és posaria sota el segon ens hauria de retornar l'excusa que contingui paraula que escriu usuari.

```python3=
@bot.inline_handler(func=lambda query: True)
def query_text(inline_query):

  	 bot.answer_inline_query(
   	 inline_query.id,
   	 results=cercar(inline_query.query)
  	 )

def cercar(consulta):
    resultats=[]
    i=0
    for acudit  in acudits:
        if (consulta in acudit): 
            i+=1
            resultats.append( types.InlineQueryResultArticle(
        			 i,
           		 acudit,
           		 types.InputTextMessageContent(acudit)
       			 )
   		 )    	 
    return resultats

bot.polling()
```

Per retornar s'ha de fer una llista d'objectes **types.InlineQueryResultArticle** amb tres camps un identificador (seqüència), el text i el text de nou com a  **types.InputTextMessageContent(text)**.
Aquí teniu una possible llista d'acudits:

```python3=
acudits=[
"Crec que estas obsessionat amb el futbol i em fas falta.  Falta! Si no t'he tocat.",
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
"En una convencion de circos un hombre pregunta: Disculpe, donde estan las hermanas siamesas? En la Sala de Juntas.",
"Que li diu el Firefox al Chrome? Que te den Mozilla"
]
```
I d'excuses:
```python3=

excuses = [
"El tren va en retras","No he canviat l'hora","El mobil no m'ha despertat","No sabia que la classe començava a les 8","Windows no funciona","El gos s'ha menjat l'arxiu","Ah! He oblidat annexar l'arxiu","No tens el document compartit?","Tinc la feina feta, però està a casa.","He fet tard perquè en ma casa fa molt de fred i el cola cao no es dissolia amb la llet.",
    "No he pogut lliurar el treball perquè han entrat a robar a ma casa i s'han emportat el meu ordinador","No estava copiant, estava mirant si el meu company ho ha fet bé.","No és que no estigui fent res, s'està descarregant un programa.","No faig la feina perquè a mi m'agrada fer els deures a casa.","He faltat a classe per temes personals, a partir de demà ja no arribaré tard i vindré tots els dies."]
```

El feu?

## 7.Tercer BOT: Bot en grup - Enquesta

Es crea igual que els altres bots però s'ha d'executar la comanda **/setjoingroups.**
Aleshores el bot s'afegeix a un grup igual que un usuari.
Podem fer que el bot interactuï només en el grup o privadament amb diversos membres del grup.
Farem només interactuï amb un sol usuari que serà el administrador.
Podem saber si amb el bot s'interactua amb un grup o privat segons el tipus missatge.chat.type

```python3=
def admin(missatge):
    global adminUser
    return ((missatge.from_user.username==adminUser) and (missatge.chat.type == "private"))
```

Practicarem en el grup [https://t.me/joinchat/C410CQ-UzEwM5hZFxlx_bQ](https://t.me/joinchat/C410CQ-UzEwM5hZFxlx_bQ)

### 8.Referències
- https://python-telegram-bot.org/
- http://piensa3d.com/tutorial-como-crear-programar-bot-telegram-python/
- http://untitled.es/bot-telegram-python-parte-2/
- https://geekytheory.com/telegram-programando-un-bot-en-python/
- https://github.com/HackLab-Almeria/clubpythonalm-taller-bots-telegram
-http://hacklabalmeria.net/actividades/2016/04/28/taller-telegram.html
- https://www.codementor.io/garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay
- https://core.telegram.org/bots
- https://khashtamov.com/en/how-to-create-a-telegram-bot-using-python/
- https://www.atareao.es/tutorial/crea-tu-propio-bot-para-telegram/
- https://github.com/eternnoir/pyTelegramBotAPI/blob/master/telebot/types.py

