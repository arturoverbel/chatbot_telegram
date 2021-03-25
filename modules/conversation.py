from settings.settings import SETTINGS, FOLDER_CONVERSATION
import random
from os import path
import json


class Conversation:
    def __init__(self,
                 identification: str,
                 name: str,
                 conversation_type: str = 'QUESTIONNAIRE',
                 ):

        # Data Firsts
        self.setting = SETTINGS[conversation_type]
        self.conversation_type = conversation_type
        self.filename = f'{FOLDER_CONVERSATION}/{identification}_{conversation_type}.json'

        # DATA Defaults
        self.identification = identification
        self.name = name
        self.questions = self.setting['QUESTIONNAIRE']
        self.words_for_end = self.setting['END_ANS_FLOW']

        # Data memory
        self.answers = []
        self.current_questions = 0

        if not self.check_file_exist():
            self.export_data()
        else:
            self.import_data()

    def receive_answer(self, text):
        if not self.has_finished():
            self.answers.append(text)

            self.export_data()

    def send_questions(self):
        q = random.choice(self.words_for_end)

        if not self.has_finished():
            if len(self.questions) > self.current_questions:
                q = self.questions[self.current_questions]
            self.current_questions += 1

            self.export_data()

        return q

    def check_file_exist(self):
        return path.exists(self.filename)

    def export_data(self):
        data = {
            'id': self.identification,
            'name': self.name,
            'questions': self.questions,
            'type': self.conversation_type,
            'answers': self.answers,
            'current_questions': self.current_questions
        }

        with open(self.filename, 'w') as outfile:
            json.dump(data, outfile)

    def import_data(self):
        with open(self.filename) as json_file:
            data = json.load(json_file)

            self.answers = data['answers']
            self.current_questions = data['current_questions']

    def send_sentences_for_end(self):
        return random.choice(self.words_for_end)

    def has_finished(self):
        return self.current_questions >= len(self.questions) + 1
