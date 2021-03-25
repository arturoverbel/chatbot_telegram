import os
import json
from modules.bot import Bot
from whatsapp.whatsapp import WhatsappApi
from settings.settings import FOLDER_RESULTS

FILE_FOREVER = "worker/run_forever.txt"
FILE_LOG_WEB = "worker/log_web.json"
FILE_LOG_INFO = "worker/log_info.json"


def clear_log():
    dir_name = f'worker/'

    for item in os.listdir(dir_name):
        if item.endswith(".json"):
            os.remove(os.path.join(dir_name, item))


def get_keep_running():
    f = open(FILE_FOREVER, "r")

    return f.read() == "1"


def get_logs():
    data_log_web = []
    if os.path.exists(FILE_LOG_WEB):
        file = open(FILE_LOG_WEB)
        data_log_web = json.load(file)

    data_log_info = {}
    if os.path.exists(FILE_LOG_INFO):
        file_info = open(FILE_LOG_INFO)
        data_log_info = json.load(file_info)

    dir_results = f'{FOLDER_RESULTS}/'
    list_results = []
    for item in os.listdir(dir_results):
        if item.endswith(".csv"):
            list_results.append((os.path.join(dir_results, item)))

    return {
        'log_web': data_log_web[::-1],
        'log_info': data_log_info,
        'results': list_results[::-1]
    }


def set_forever():
    f = open(FILE_FOREVER, "w")
    f.write("1")
    f.close()


def stop_forever():
    f = open(FILE_FOREVER, "w")
    f.write("0")
    f.close()


class WorkerBot:
    def __init__(self):
        self.whatsapp = None

        self.bot = Bot()

        self.log_web = []
        self.log_info = {}

        self.init()

    def init(self):
        self.whatsapp = WhatsappApi()

        self.bot.restart()
        self.log_web = []
        self.log_info = {}

        clear_log()

    def run(self):
        set_forever()

        while get_keep_running():
            for message in self.whatsapp.get_messages(restart_index=True):
                chat_id = message["chatId"]
                name = message["senderName"]
                text = message["body"]

                tt = text
                if "media/" in tt:
                    tt = f'<a href="{tt}">{tt}</a>'
                self.add_log_web(f'Answer "{tt}" received from {name}')
                self.add_log_info(chat_id, name, text, is_question=False)

                question = self.bot.receive_message(chat_id, name, text)

                response = self.whatsapp.send_message(chat_id, question)
                self.add_log_web(f'Question "{question}" sent to {name}')
                self.add_log_info(chat_id, name, question)

        self.bot.export_results()

        self.restart()

    def add_log_web(self, text):
        print(text)
        self.log_web.append(text)

        file = open(FILE_LOG_WEB, 'w')
        json.dump(self.log_web, file)

    def add_log_info(self, chat_id, name, text, is_question=True):
        if chat_id in self.log_info:
            if is_question:
                self.log_info[chat_id]["questions"].append(text)
            else:
                self.log_info[chat_id]["answers"].append(text)
        else:
            self.log_info[chat_id] = {
                "name": name,
                "text": text,
                "questions": [],
                "answers": []
            }

        file = open(FILE_LOG_INFO, 'w')
        json.dump(self.log_info, file)

    def restart(self):
        f = open(FILE_FOREVER, "w")
        f.write("0")
        f.close()

        self.init()

        set_forever()

        self.run()

