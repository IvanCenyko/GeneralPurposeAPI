import json, requests
from bs4 import BeautifulSoup


pagina = requests.get("https://qpaso.ar/")
soup = BeautifulSoup(pagina.content, 'html.parser')

# filtro los apartado de noticias que tengan un ID, queda un elemento de lista por
# cada medio de comunicacion
news_soup = soup.find(id = "news").find_all("div", id=True)
news2_soup = soup.find(id = "news2").find_all("div", id=True)


# para cada medio de comunicacion
for medio in news_soup:
    # busco el nombre
    nombre = medio["id"]
    # busco los titulares
    noticias = medio.find_all("h3")
    
    print(nombre)
    # busco el texto de cada estructura de titular
    for noticia in noticias:
        # convierto a texto y elimino posibles type errors
        print(noticia.text.replace('\n', ' ').replace('  ', ''))
    print('---------------------------------------------------')

# repito para la 2da tanda de medios de comunicacion
for new in news2_soup:
    medio = new["id"]
    noticias = new.find_all("h3")
    
    print(medio)
    for noticia in noticias:
        print(noticia.text.replace('\n', ' ').replace('  ', ''))
    print('---------------------------------------------------')



