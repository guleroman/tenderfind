import requests

def Speller(stroke):
    try:
        if type(stroke) is list:
            stroke = " ".join(stroke)
        status = 200
        params = {'text': stroke, 'lang':"rus"}
        r = requests.get('http://speller.yandex.net/services/spellservice.json/checkText', params=params)
        data = r.json()
        for co in data:
            if co['s'] != []:
                stroke = stroke.replace(stroke[co['pos']:co['pos']+co['len']],co['s'][0].lower())
        return(stroke, status)
    except:
        status = 422
        return (stroke, status)

def Sinonims(query):
    try:
        sinonims = []
        if type(query) is list:
            query = " ".join(query)
        status = 200
        params = {'text': query, 'lang':"ru-ru","key":"dict.1.1.20180822T091221Z.f831c0a5a638825e.290baebf00efbd973a2273af5a197d0addcef9f3"}
        r = requests.get('https://dictionary.yandex.net/api/v1/dicservice.json/lookup', params=params)
        data = r.json()
        sinonims.append(query)
        sinonims.append(data['def'][0]['tr'][0]['text'])
        for syn in data['def'][0]['tr'][0]['syn']:
            sinonims.append(syn['text'])
        #for co in data:
        #    if co['s'] != []:
        #        stroke = stroke.replace(stroke[co['pos']:co['pos']+co['len']],co['s'][0].lower())
        return(sinonims, status)
    except:
        status = 422
        return (sinonims, status)