from datetime import datetime
import glob
import params
import json
import csv
import os

## exporta resultados
def return_question_ids():
    q = []
    for idx in enumerate(params.QUESTIONARY):
        q.append("Q" + str(idx[0]+1))

    return q


def return_name_file():
    n = datetime.now()
    year = n.strftime("%Y")
    month = n.strftime("%m")
    day = n.strftime("%d")
    hour = n.strftime("%H")
    min = n.strftime("%M")

    return "results/results_" + year + "_" + month + "_" + day + "_" + hour + "_" + min + ".csv"


csv_file = return_name_file()
data_before = ""


def export_results():
    global data_before
    
    print("CURRENT_FLOWS_BY_IDS:")
    print(params.CURRENT_FLOWS_BY_IDS)

    if len(params.CURRENT_FLOWS_BY_IDS) == 0:
        return

    results = []
    for ID_CHAT, msn in params.CURRENT_FLOWS_QUESTIONS_BY_IDS.items():
        

        data_to_insert = {
            "ID": ID_CHAT,
            "name": msn["name"]
        }
        for idx, question in enumerate(return_question_ids()):
            data_to_insert[question] = ""

            if len(params.CURRENT_FLOWS_BY_IDS[ID_CHAT]) > idx+1:
                data_to_insert[question] = params.CURRENT_FLOWS_BY_IDS[ID_CHAT][idx+1]['answer']

        results.append(data_to_insert)

    json_now = json.dumps(results)
    if json_now == data_before:
        return

    csv_columns = ["ID", "name"] + return_question_ids()
    print(results)

    try:
        # if os.path.exists(csv_file):
        #        os.remove(csv_file)
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for dataa in results:
                writer.writerow(dataa)

    except IOError:
        print("I/O error")

    print("Results exported")
    data_before = json_now


def get_all_results():
    files = list(filter(os.path.isfile, glob.glob('results/' + "*")))
    files.sort(key=lambda x: os.path.getmtime(x))
    files.reverse()
    
    return files