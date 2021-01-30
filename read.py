from params import URL
import requests
import json


def update():
    respuesta = requests.get(URL + "getUpdates")

    mensajes_js = respuesta.content.decode("utf8")

    mensajes_diccionario = json.loads(mensajes_js)

    return mensajes_diccionario['result']

def info_mensaje(mensaje):

    print(mensaje["message"])
    if "text" in mensaje["message"]:
        tipo = "texto"
    elif "sticker" in mensaje["message"]:
        tipo = "sticker"
    elif "animation" in mensaje["message"]:
        tipo = "animacion" #Nota: los GIF cuentan como animaciones
    elif "photo" in mensaje["message"]:
        tipo = "foto"
    else:
        tipo = "otro"

    #texto = mensajes["result"][indice]["message"]["text"]
    persona = mensaje["message"]["from"]["first_name"]
    id_chat = mensaje["message"]["chat"]["id"]
    id_update = mensaje["update_id"]

    return tipo, id_chat, persona, id_update
