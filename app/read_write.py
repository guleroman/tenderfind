import json

def readData(token=None):
    with open('history.json', 'r',encoding='utf-8') as fh: #открываем файл с данными о исполнителях на чтение
        history = json.load(fh)
    if token is not None: 
        return(history[token])
    else:
        return(history)

def writeData(new):
    history_old = readData()
    history_old.update(new)
    with open("history.json", "w", encoding='utf-8') as write_file:
        json.dump(history_old, write_file)
    return ('ok')

def readHtml(nameHtml):
    with open(nameHtml, 'r',encoding='utf-8') as fh: #открываем файл с даннымина чтение
        codeHtml = fh.readline()
    return(codeHtml)