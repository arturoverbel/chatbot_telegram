import json

json_config_file = 'config/config.json'

def validate_run_forever():
    with open(json_config_file) as json_file:
        conf = json.load(json_file)

    return conf["run_forever"] == 1

def set_run_forever_again():
    json_file = open(json_config_file)
    conf = json.load(json_file)

    json_file.close()
    
    conf["run_forever"] = 1

    with open(json_config_file, 'w') as outfile:
        json.dump(conf, outfile)

def stop_forever():
    json_file = open(json_config_file)
    conf = json.load(json_file)

    json_file.close()
    
    conf["run_forever"] = 0

    with open(json_config_file, 'w') as outfile:
        json.dump(conf, outfile)
    
    return "1"