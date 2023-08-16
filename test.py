import json, os

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

def json_escritor(**kwargs):

    with open(kwargs['direction'], 'w') as js:
        json.dump(kwargs['dict'], js)

def json_borrador(direction:str):
    with open(r'./dolar.json', 'w') as js:
        js.truncate()

def json_lector(direction:str):
    with open(direction, 'r') as js:
        return json.load(js)

json_borrador(r'./dolar.json')
json_escritor(direction=r'./dolar.json', dict={"nashe":"nashe"})
print(json_lector(r'./dolar.json'))