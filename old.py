import json
import requests

TOKEN = "1500266223:AAHTT0AoygfTSTrCl0XNUXfMu8lH5nTFb6E"
URL = "https://api.telegram.org/bot" + TOKEN + "/"

## Llamar el servicio para los mensajes
def update():
    respuesta = requests.get(URL + "getUpdates")

    mensajes_js = respuesta.content.decode("utf8")

    mensajes_diccionario = json.loads(mensajes_js)

    return mensajes_diccionario
## Atrapando datos deseados
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

    persona = mensaje["message"]["from"]["first_name"]
    id_chat = mensaje["message"]["chat"]["id"]
    id_update = mensaje["update_id"]

    return tipo, id_chat, persona, id_update
## Ejecutar lo anterior
def leer_mensaje():
    mensajes = update()
    indice = len(mensajes["result"])-1

    texto = mensajes["result"][indice]["message"]["text"]
    persona = mensajes["result"][indice]["message"]["from"]["first_name"]
    id_chat = mensajes["result"][indice]["message"]["chat"]["id"]

    return id_chat, persona, texto

def enviar_mensaje(idchat, texto):
    requests.get(URL + "sendMessage?text=" + texto + "&chat_id=" + str(idchat))


last_idchat, last_nombre, last_texto = "", "", ""
write = True
first = True

while(True):
    idchat, nombre, texto = leer_mensaje()

    if not (last_idchat == idchat and last_nombre == nombre and last_texto == texto):
        write = True
        print(nombre + " (id: " + str(idchat) + ") ha escrito: " + texto)
    else:
        write = False

    last_idchat = idchat
    last_nombre = nombre
    last_texto = texto

    if write == False or first:
        first = False
        continue

    if "hola" in texto.lower():
        texto_respuesta = "Hola, " + nombre + "!"
        enviar_mensaje(idchat, texto_respuesta)
    elif "adios" in texto.lower():
        texto_respuesta = "Hasta pronto!"
        enviar_mensaje(idchat, texto_respuesta)
