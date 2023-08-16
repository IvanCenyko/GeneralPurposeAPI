import requests, queue, threading, time, random, telebot
from bs4 import BeautifulSoup
import files

#bot token
bot = telebot.TeleBot('6204169915:AAHO-Nh2HgMZk3h-NlyrNT1tLb4ioU1D44k')
#multithreading init
q = queue.Queue()
#txt
users_subs = r"./users.txt"
frases_peronistas = r"./frases.txt"
dolar_registrado = r"./dolar.json"


def blue():
    # request
    dolar_request = requests.get('https://dolarhoy.com/')
    # html crudo
    soup = BeautifulSoup(dolar_request.content, 'html.parser')
    # divs con clase tile is-child
    divs = soup.find_all(class_='tile is-child')
    # primer resultado, es decir, dolar blue
    div_dolar = divs[0]
    # busco en la div del blue la parte de venta
    venta_soup = div_dolar.find(class_='venta')
    # busco en la parte de venta el precio, y filtro solo texto
    venta = venta_soup.find(class_='val').text

    # repito ultimos dos pasos pero con compra
    compra_soup = divs[0].find(class_='compra')
    compra = compra_soup.find(class_='val').text

    # quito el '$' y convierto a int
    venta = int(venta.replace('$', ''))
    compra = int(compra.replace('$', ''))

    try:
        files.json_borrador(dolar_registrado)
    except:
        pass
    files.json_escritor(direction=dolar_registrado, dict={"venta": venta, "compra": compra})
    return {"venta": venta, "compra": compra}



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

        if not message.chat.id in files.txt_lector(users_subs):
            files.txt_escritor(users_subs, message.chat.id)
            bot.reply_to(message, text='Añadido')
        else:
            bot.reply_to(message, text='Ya estás añadido')

    @bot.message_handler(commands=["advlist"])
    def advlist(message):
        bot.reply_to(message, text= str(files.txt_lector(users_subs)))

    @bot.message_handler(commands=["peron", "peronismo", "frase", "fraseperoncha", "fraseperonista"])
    def frase_peronista(message):
        bot.reply_to(message, f"""
{random.choice(files.txt_lector(frases_peronistas))}
- Juan Domingo Perón
""")

    @bot.message_handler(func=lambda message: True)
    def unknown_command(message):
        bot.reply_to(message, "No te entendí, usá /help para ver la lista de comandos!")


    bot.infinity_polling()



def message_send():
    value = int(files.json_lector(dolar_registrado)["venta"])
    single_use = True
    while 1:
        if  blue()['venta'] == 505 and single_use:
            for user in files.txt_lector(users_subs):
                bot.send_message(chat_id = user, text='''
EL DOLAR LLEGÓ A 505 - ARCTIC MONKEYS
https://www.youtube.com/watch?v=qU9mHegkTc4''')
            single_use = False

        elif blue()['venta'] >= value + 10 and files.txt_lector(users_subs):
            value = files.json_lector(dolar_registrado)["venta"]
            for user in files.txt_lector(users_subs):
                bot.send_message(chat_id = user, text= f'El dolar subió a {value} VIVA PERÓN ✌️. Está {blue()["venta"]}')

        elif blue()['venta'] <= value - 10 and files.txt_lector(users_subs):
            value = files.json_lector(dolar_registrado)["venta"]
            for user in files.txt_lector(users_subs):
                bot.send_message(chat_id = user, text= f'El dolar bajó a {value} VIVA PERÓN ✌️. Está {blue()["venta"]}')


        if not blue()['venta'] == 505:
            single_use = True


t1 = threading.Thread(target=telegram_bot)
t2 = threading.Thread(target=message_send)
t1.start()
t2.start()
