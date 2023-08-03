import requests, queue, threading, time, random, telebot

#bot token
bot = telebot.TeleBot('6204169915:AAHO-Nh2HgMZk3h-NlyrNT1tLb4ioU1D44k')
#multithreading init
q = queue.Queue()
#txt
users_subs = r"./users.txt"
frases_peronistas = r"./frases.txt"
dolar_registrado = r"./dolar.txt"

def lector(direction:str):
    file = open(direction, "r+")
    file_read = file.read()

    line = ""
    lines = []
    letters = list(file_read)

    for digit in letters:
        if not digit == "\n":
            line += digit
        if digit == "\n":
            lines.append(line)
            line = ""
    return lines

def escritor(direction:str, information):
    file = open(direction, "a")
    file.write(f"{information}\n")


def blue():
    moneda = requests.get('https://api.bluelytics.com.ar/v2/latest').json()
    return {
        'venta' : int(moneda['blue']['value_sell']),
        'compra' : int(moneda['blue']['value_buy'])
    }



def telegram_bot():
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.reply_to(message, text=f'''
Hola soy InzaBot, usá /help para lista de comandos ✌️
CFK 2023!
''')


    @bot.message_handler(commands=['help'])
    def help(message):
        bot.reply_to(message, text= """
Comandos:
/bluenow: el dolar ahora
/addme: te añade a la lista de aviso de subida de dolar
/peron, peronismo, frase, fraseperoncha, fraseperonista: Frase random de Perón
""")


    @bot.message_handler(commands=['bluenow'])
    def bluenow(message):
        bot.reply_to(message, text=f'''
El dólar está {blue()['venta']} en venta y {blue()['compra']} en compra.
VIVA PERÓN ✌️
''')

    @bot.message_handler(commands=['addme'])
    def blueadv(message):

        if not str(message.chat.id) in lector(users_subs):
            escritor(users_subs, message.chat.id)
            bot.reply_to(message, text='Añadido')
        else:
            bot.reply_to(message, text='Ya estás añadido')

    @bot.message_handler(commands=["advlist"])
    def advlist(message):
        bot.reply_to(message, text= str(lector(users_subs)))

    @bot.message_handler(commands=["peron", "peronismo", "frase", "fraseperoncha", "fraseperonista"])
    def frase_peronista(message):
        bot.reply_to(message, f"""
{random.choice(lector(frases_peronistas))}
- Juan Domingo Perón
""")

    @bot.message_handler(func=lambda message: True)
    def unknown_command(message):
        bot.reply_to(message, "No te entendí, usá /help para ver la lista de comandos!")


    bot.infinity_polling()



def message_send():
    value = int(lector(dolar_registrado)[0])
    single_use = True
    while 1:
        if  blue()['venta'] == 505 and single_use:
            for user in lector(users_subs):
                bot.send_message(chat_id = user, text='''
EL DOLAR LLEGÓ A 505 - ARCTIC MONKEYS
https://www.youtube.com/watch?v=qU9mHegkTc4''')
            single_use = False

        elif blue()['venta'] >= value + 10 and lector(users_subs):
            for user in lector(users_subs):
                bot.send_message(chat_id = user, text= f'El dolar subió a {value} VIVA PERÓN ✌️. Está {blue()["venta"]}')
            value += 10
        elif blue()['venta'] <= value - 10 and lector(users_subs):
            value -= 10
            for user in lector(users_subs):
                bot.send_message(chat_id = user, text= f'El dolar bajó a {value} VIVA PERÓN ✌️. Está {blue()["venta"]}')


        if not blue()['venta'] == 505:
            single_use = True


t1 = threading.Thread(target=telegram_bot)
t2 = threading.Thread(target=message_send)
t1.start()
t2.start()
