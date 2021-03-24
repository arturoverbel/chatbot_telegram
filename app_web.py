from flask import Flask, render_template, Response, send_from_directory
from worker.worker import WorkerBot
import json


app = Flask(__name__)
worker_bot = WorkerBot()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/restart')
def restart():
    worker_bot.restart()

    return '1'


@app.route('/log_web')
def get_log_web():
    list_log = worker_bot.log_web[::-1]
    return Response(json.dumps(list_log),  mimetype='application/json')


@app.route('/log_info')
def get_log_info():
    return Response(json.dumps(worker_bot.log_info),  mimetype='application/json')


@app.route('/results/<path:path>')
def data_results(path):
    return send_from_directory('results', path)


@app.route('/media/<path:path>')
def data_media(path):
    return send_from_directory('media', path)


if __name__ == '__main__':
    app.run()

