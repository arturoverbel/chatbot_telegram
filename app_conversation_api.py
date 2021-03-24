from flask import Flask, request, jsonify
from modules.bot import Bot
import json

app = Flask(__name__)


@app.route('/restart')
def restart():
    bot = Bot()
    bot.restart()

    return 'restarted'


@app.route('/export')
def export():
    bot = Bot()
    bot.export_results()

    return 'exported'


@app.route('/receive', methods=['POST'])
def receive():
    bot = Bot()
    content = request.json

    response = bot.receive_message(content["id"], content["name"], content["answer"])

    return response


if __name__ == '__main__':
    app.run()

