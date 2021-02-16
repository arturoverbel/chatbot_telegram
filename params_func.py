from datetime import datetime
import requests
import params
import json
import logs


def set_params(datas):

    for data in datas:
        if data["author"] == "573197612585@c.us":
            continue

        ID_CHAT = data["chatId"]
        ID_MESSAGE = data["id"]

        data_to_save = {
            "id": ID_MESSAGE,
            "name": data["senderName"],
            "chatid": ID_CHAT,
            "date": data["time"],
            "type": "text",
            "answer": data["body"]
        }

        # FILTER TIME
        elapsedTime = datetime.now() - datetime.fromtimestamp(data_to_save["date"])
        if elapsedTime.total_seconds() > params.SECONDS_MIN:
            continue

        if ID_CHAT not in params.CURRENT_FLOWS_BY_IDS:
            params.CURRENT_FLOWS_BY_IDS[ID_CHAT] = []
            params.CURRENT_FLOWS_QUESTIONS_BY_IDS[ID_CHAT] = []
            params.CURRENT_FLOWS_BY_IDS_PARAMS[ID_CHAT] = {
                "finished": False
            }

        found = False
        for chat in params.CURRENT_FLOWS_BY_IDS[ID_CHAT]:
            if chat["id"] == ID_MESSAGE:
                found = True
                break
        if found:
            continue

        if "https://" in data["body"]:
            data_to_save["type"] = "link"
            data_to_save["answer"] = get_file(data["body"])

        txt = "<br>" + str(ID_CHAT) + "<br> -> <br>bot<br>: " + data_to_save["answer"]
        logs.log(txt)

        params.CURRENT_FLOWS_BY_IDS[ID_CHAT].append(data_to_save)


def get_file(file_link):
    # Get File
    file_stream = requests.get(file_link)

    now = datetime.now()
    key_time = str(now.year)+"_"+str(now.month)+"_"+str(now.day) + \
        "_"+str(now.hour)+"_"+str(now.minute)
    file_path = "media/" + key_time + "_" + file_link.split("/")[-1]

    open(file_path, 'wb').write(file_stream.content)

    print("File downloaded: ", file_path)
    return file_path
