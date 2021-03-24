from modules.bot import Bot
from whatsapp.whatsapp import WhatsappApi

FILE_FOREVER = "worker/run_forever.txt"


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

    def run(self):
        while self.get_keep_running():
            for message in self.whatsapp.get_messages(restart_index=True):
                chat_id = message["chatId"]
                name = message["senderName"]
                text = message["body"]

                self.add_log_web(f'Answer "{text}" received from {name}')
                self.add_log_info(chat_id, name, text, is_question=False)

                question = self.bot.receive_message(chat_id, name, text)

                response = self.whatsapp.send_message(chat_id, question)
                self.add_log_web(f'Question "{question}" sent to {name}')
                self.add_log_info(chat_id, name, text)

        self.bot.export_results()

    def add_log_web(self, text):
        print(text)
        self.log_web.append(text)

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

    def restart(self):
        f = open(FILE_FOREVER, "w")
        f.write("0")
        f.close()

        self.init()

        f = open(FILE_FOREVER, "w")
        f.write("1")
        f.close()

        self.run()

    def get_keep_running(self):
        f = open(FILE_FOREVER, "r")

        return f.read() == "1"

