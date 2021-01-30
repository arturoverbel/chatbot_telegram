from flask import Flask, render_template, Response, send_from_directory
from chatbot import run_chatbot, stop_chatbot
from results import get_all_results
from logs import get_all
import threading
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start():
    x = threading.Thread(target=run_chatbot, daemon=True)
    x.start()

    return '1'

@app.route('/stop')
def stop():
    return stop_chatbot()

@app.route('/logs')
def logs():
    return get_all()

@app.route('/results')
def results():
    d = get_all_results()
    return Response(json.dumps(d),  mimetype='application/json')

@app.route('/results/<path:path>')
def data_results(path):
    return send_from_directory('results', path)

if __name__ == '__main__':
    app.run()

