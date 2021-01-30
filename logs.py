logs_file = 'logs/log.txt'

def log(text):

    print(text)
    with open(logs_file, "a") as file_object:
        file_object.write("<br>\n")
        file_object.write(text)
    
    return 1

def clean():
    f = open(logs_file, 'r+')
    f.truncate(0)
    f.close()


def get_all():
    file = open(logs_file, mode='r') 
    all_of_it = file.read()
    file.close()

    x = all_of_it.split("<br>") 
    x.reverse()
    strr = "<br>".join(x)

    return strr