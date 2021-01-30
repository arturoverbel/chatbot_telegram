from datetime import datetime
import requests
import params
import json
import logs

def set_params(datas):

    for data in datas:
        ID_CHAT = data["message"]["chat"]["id"]
        ID_MESSAGE = data["update_id"]

        data_to_save = {
            "update_id": data["update_id"],
            "name": data["message"]["chat"]["first_name"],
            "id": data["message"]["chat"]["id"],
            "date": data["message"]["date"],
            "type": "",
            "answer": "other"
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
            if chat["update_id"] == ID_MESSAGE:
                found = True
                break
        if found:
            continue
        
        if "text" in data["message"]:
            data_to_save["type"] = "text"
            data_to_save["answer"] = data["message"]["text"]
        elif "voice" in data["message"]:
            data_to_save["type"] = "voice"
            data_to_save["answer"] = get_file(data["message"]["voice"]["file_id"])
        elif "photo" in data["message"]:
            data_to_save["type"] = "photo"
            data_to_save["answer"] = get_file(data["message"]["photo"][0]["file_id"])
        
        txt = "<br>" + str(ID_CHAT) + "<br> -> <br>bot<br>: " + data_to_save["answer"]
        logs.log(txt)

        params.CURRENT_FLOWS_BY_IDS[ID_CHAT].append(data_to_save)

def get_file(file_id):
    ## Get File Path
    response = requests.get(params.URL + "getFile?file_id=" + file_id)
    response_str = response.content.decode("utf8")

    response_dic = json.loads(response_str)

    file_path = response_dic['result']['file_path']
    

    ## Get File
    file_stream = requests.get(params.URL_FILE + file_path)

    open(file_path, 'wb').write(file_stream.content)

    print("File downloaded: ", file_path)
    return file_path