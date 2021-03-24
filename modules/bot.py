import os
from datetime import datetime
from settings.settings import FOLDER_CONVERSATION, FOLDER_RESULTS
from modules.conversation import Conversation
import json
import csv


class Bot:
    def __init__(self, conversation_type: str = "TEST"):
        self.conversation_type = conversation_type

    def restart(self):
        self.__reset_memory_conversations()

    def export_results(self):
        self.__export_results()

    def receive_message(self, identification, name, text):
        conversation = Conversation(identification, name, self.conversation_type)

        conversation.receive_answer(text)

        return conversation.send_questions()

    def __reset_memory_conversations(self):
        dir_name = f'{FOLDER_CONVERSATION}/'

        for item in os.listdir(dir_name):
            if item.endswith(".json"):
                os.remove(os.path.join(dir_name, item))

    def __export_results(self):
        dir_name = f'{FOLDER_CONVERSATION}/'
        results = []
        print("-- EXPORTING ---")
        for item in os.listdir(dir_name):
            if item.endswith(".json"):
                with open(f'{dir_name}{item}') as json_file:
                    data = json.load(json_file)

                    identification = data["id"]
                    name = data["name"]

                    conversation = Conversation(identification, name, self.conversation_type)

                    columns_data = conversation.questions.copy()
                    values_data = conversation.answers.copy()

                    if not conversation.has_finished():
                        print(f'Conversation {identification} has not finished')
                        continue

                    columns_data.insert(0, "-")
                    values_data.append("-")

                    data_to_insert = {
                        "ID": identification,
                        "name": name
                    }

                    for idx, value in enumerate(columns_data):
                        column_name = "-" if value == "-" else f'Q{idx}'
                        value_name = values_data[idx]

                        data_to_insert[column_name] = value_name

                    results.append(data_to_insert)

        keys = results[0].keys()
        filename = self.__return_name_file()
        with open(f'{FOLDER_RESULTS}/{filename}', 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(results)

    def __return_name_file(self):
        n = datetime.now()
        year = n.strftime("%Y")
        month = n.strftime("%m")
        day = n.strftime("%d")
        hour = n.strftime("%H")
        minute = n.strftime("%M")

        return "results_" + year + "_" + month + "_" + day + "_" + hour + "_" + minute + ".csv"
