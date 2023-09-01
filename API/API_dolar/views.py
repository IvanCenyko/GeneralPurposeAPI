from django.shortcuts import render
from django.http import JsonResponse
from bs4 import BeautifulSoup
import requests

def dolar_blue(request):
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

    return JsonResponse({"venta": venta, "compra": compra})