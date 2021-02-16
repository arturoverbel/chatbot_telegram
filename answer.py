from datetime import datetime
import params
import requests
import logs


def send_answers():

    for ID_CHAT, messages in params.CURRENT_FLOWS_BY_IDS.items():
        if params.CURRENT_FLOWS_BY_IDS_PARAMS[ID_CHAT]["finished"]:
            continue

        num_messages = len(messages)
        num_questions = len(params.QUESTIONARY) + 1

        # Init
        if num_messages >= num_questions:
            send_text(ID_CHAT, params.END_ANS_FLOW[0])
            params.CURRENT_FLOWS_BY_IDS_PARAMS[ID_CHAT]["finished"] = True
            continue

        # for message in messages:
        question = params.QUESTIONARY[num_messages-1]
        send_text(ID_CHAT, question)


def send_text(idchat, texto):
    if texto in params.CURRENT_FLOWS_QUESTIONS_BY_IDS[idchat]:
        return

    params.CURRENT_FLOWS_QUESTIONS_BY_IDS[idchat].append(texto)

    requests.get(params.URL_SEND + "&chatId=" + str(idchat) + "&body=" + texto)

    txt = "(bot) -> (" + str(idchat) + "): " + texto
    logs.log(txt)
