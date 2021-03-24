from flask import Flask, request, jsonify, Response
from whatsapp.whatsapp import WhatsappApi
import json

app = Flask(__name__)
whatsapp = WhatsappApi()


@app.route('/messages')
def message():
    messages = whatsapp.get_messages()

    return Response(json.dumps(messages),  mimetype='application/json')


@app.route('/send', methods=['POST'])
def send():
    content = request.json

    response = whatsapp.send_message(content["id_chat"], content["text"])

    return Response(json.dumps(response),  mimetype='application/json')


if __name__ == '__main__':
    app.run()

