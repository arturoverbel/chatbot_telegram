from settings.settings_whatsapp import WHATSAPP_SETTINGS
import requests
import json
from os import path


class WhatsappApi:
    def __init__(self):
        self.URL_GET = WHATSAPP_SETTINGS['URL_GET']
        self.URL_SEND = WHATSAPP_SETTINGS['URL_SEND']
        self.index_first_time = 0

        self.first_time()

        print("---------------------------------------------------------")
        print("Init Whatsapp API R2 =D ")
        print(f'Start message since {self.index_first_time}')

    def first_time(self):
        self.restart_index(self.__get_last_messages()[-1]['messageNumber'])

    def restart_index(self, index: int):
        self.index_first_time = index

    def __get_last_messages(self):
        response = requests.get(self.URL_GET)

        messages = response.content.decode("utf8")

        messages_dict = json.loads(messages)

        return messages_dict['messages']

    def get_messages(self, restart_index=False):
        messages = self.__get_last_messages()[::-1]
        messages_results = []

        last_index = 0
        for message in messages:
            if message['messageNumber'] == self.index_first_time:
                break

            if message['fromMe']:
                continue

            last_index = message['messageNumber']
            messages_results.append(message)

            if "https://" in message["body"]:
                message["body"] = self.get_file(message["body"])

        if restart_index and last_index != 0:
            self.restart_index(last_index)

        return messages_results

    def send_message(self, chatID: int, text: str):
        data_response = requests.get(self.URL_SEND + f'&chatId={str(chatID)}&body={text}')

        return data_response.status_code == 200

    def get_file(self, file_link):
        """
        now = datetime.now()
        key_time = f'{str(now.year)}_{str(now.month)}_{str(now.day)}_{str(now.hour)}_{str(now.minute)}'
        """
        file_path = f'media/{file_link.split("/")[-1]}'

        if path.exists(file_path):
            return file_path

        # Get File
        file_stream = requests.get(file_link)

        open(file_path, 'wb').write(file_stream.content)

        print(f'File downloaded: {file_path}')

        return file_path
