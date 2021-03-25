from flask import Flask, render_template, Response, send_from_directory
import worker.worker as w
import json


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/restart')
def restart():
    w.stop_forever()

    return '1'


@app.route('/logs')
def get_log_web():
    list_log = w.get_logs()
    return Response(json.dumps(list_log),  mimetype='application/json')


@app.route('/modules/results/<path:path>')
def data_results(path):
    return send_from_directory('modules/results', path)


@app.route('/media/<path:path>')
def data_media(path):
    return send_from_directory('media', path)


if __name__ == '__main__':
    app.run()

