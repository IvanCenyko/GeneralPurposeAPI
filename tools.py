import json, requests
from bs4 import BeautifulSoup

def txt_lector(direction:str):
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

def txt_escritor(direction:str, information):
    file = open(direction, "a")
    file.write(f"{information}\n")

def json_escritor(**kwargs):

    with open(kwargs['direction'], 'w') as js:
        json.dump(kwargs['dict'], js)

def json_borrador(direction:str):
    with open(r'./dolar.json', 'w') as js:
        js.truncate()

def json_lector(direction:str):
    with open(direction, 'r') as js:
        return json.load(js)
    
def blue(save_dir):
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
        json_borrador(save_dir)
    except:
        pass
    json_escritor(direction=save_dir, dict={"venta": venta, "compra": compra})
    return {"venta": venta, "compra": compra}



