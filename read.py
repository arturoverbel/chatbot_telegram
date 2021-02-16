from params import URL_GET
import requests
import json


def update():
    respuesta = requests.get(URL_GET)

    mensajes_js = respuesta.content.decode("utf8")

    mensajes_diccionario = json.loads(mensajes_js)

    return mensajes_diccionario['messages']
