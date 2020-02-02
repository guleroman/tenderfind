import re
import os
import json
from collections import Counter
import pandas as pd
import pymorphy2
import operator
import time
from read_write import readData
#from recognition_themes2 import moodDetection 
from speller import Speller, Sinonims
morph = pymorphy2.MorphAnalyzer()

global rules
rules = pd.read_pickle('../test_data/rules.pkl')

global data
data = pd.read_excel('../test_data/data.xlsx')

global data_2
data_2 = pd.read_pickle('../test_data/data_tag_1.pkl')

listt = ('вот так').split(' ')

global stop_words
stop_words = Counter(listt)

def stopfuckingwords(words, stop_words):
    return (list(Counter(words) - stop_words))

def text_preprocess(text):
    text = text.lower()
    ll = re.findall(r'\w+', text)
    print(f'было - {ll}')
    ll,code = Speller(ll)# Разбивка строки на слова, без учета знаков препинания.
    ls = [morph.parse(word)[0].normal_form for word in ll if len(word) >= 4] # Приведение слов, длина которых >= 3  к нормальной форме
    ls = stopfuckingwords(ls,stop_words)
    
    print(f'стало - {ls}')
    #print(f'Слова после предобработки и исключения стоп слов - {ls}')
    sp = ' '.join(ls) # Склеиваем слова в строку
    return (sp)

def get_bigrams(text):
    bigrams = [b for l in text for b in zip(l.split(" ")[:-1], l.split(" ")[1:])]
    bigramss = []
    for i in bigrams:
        bigramss.append(f"{i[0]}_{i[1]}")
    return(bigramss)

def get_tags(text):
    tags = text_preprocess(text)
    bigrams = get_bigrams([tags])
    bigrams = " ".join(bigrams)
    return(set((tags + " " + bigrams).split()))

def get_similar_tovar(class_p=None,class_t=None,text=None):
    start_time = time.time()
    some = {}
    similar_tovar_id = []
    text_set = get_tags(f'{text}')
    newset = list(data_2['tag_1'])
    data_id = list(data_2['Id'])
    similar_tovar = []
    similar_tovar_final = []
    for i in range(len(data_2)):
        try:
            some.update({data_id[i]:len(newset[i] & text_set)})
        except:
            some.update({data_id[i]:0})
    #idd = max(some,key=some.get)
    #print(idd)
    ids = sorted(some.items(),key=operator.itemgetter(1),reverse=True)[:20]
    for i in ids:
        if i[1]>0:
            similar_tovar_id.append(i[0])
    #return(data_2['Наименование'][idd])
    
    for id_ in similar_tovar_id:
        similar_tovar.append({"Id":str(data[data['Id'] == id_]['Id'].values[0]).replace("nan","-1"),
         "Наименование":str(data[data['Id'] == id_]['Наменование'].values[0]).replace("nan","-1"),
         "Производитель":str(data[data['Id'] == id_]['Производитель'].values[0]).replace("nan","-1"),
         "Страна происхождения":str(data[data['Id'] == id_]['Страна происхождения'].values[0]).replace("nan","-1"),
         "Вид продукции":str(data[data['Id'] == id_]['Вид продукции'].values[0]).replace("nan","-1"),
         "Вид товаров":str(data[data['Id'] == id_]['Вид товаров'].values[0]).replace("nan","-1"),
         "Длина":str(data[data['Id'] == id_]['Длина'].values[0]).replace("nan","-1"),
         "Ширина":str(data[data['Id'] == id_]['Ширина'].values[0]).replace("nan","-1"),
         "Высота":str(data[data['Id'] == id_]['Высота'].values[0]).replace("nan","-1"),
         "Материал":str(data[data['Id'] == id_]['Материал'].values[0]).replace("nan","-1"),
         "Диаметр":str(data[data['Id'] == id_]['Диаметр'].values[0]).replace("nan","-1"),
         "Гарантийный срок":str(data[data['Id'] == id_]['Гарантийный срок'].values[0]).replace("nan","-1"),
         "Цвет":str(data[data['Id'] == id_]['Цвет'].values[0]).replace("nan","-1"),
         "Вес":str(data[data['Id'] == id_]['Вес'].values[0]).replace("nan","-1"),
         "Объем":str(data[data['Id'] == id_]['Объем'].values[0]).replace("nan","-1"),
         "Количество действующих оферт":str(data[data['Id'] == id_]['Количество действующих оферт'].values[0]).replace("nan","-1"),
         "Сумма в составе контрактов":str(data[data['Id'] == id_]['Сумма в составе контрактов'].values[0]).replace("nan","-1"),
         "Количество контрактов":str(data[data['Id'] == id_]['Количество контрактов'].values[0]).replace("nan","-1")})
    similar_tovar = filters(class_p=class_p, class_t=class_t, similar_tovar = similar_tovar)
    for id_ in similar_tovar['Id']:
        similar_tovar_final.append({"Id":str(similar_tovar[similar_tovar['Id'] == id_]['Id'].values[0]).replace("nan","-1"),
         "Наименование":str(similar_tovar[similar_tovar['Id'] == id_]['Наименование'].values[0]).replace("nan","-1"),
         "Производитель":str(similar_tovar[similar_tovar['Id'] == id_]['Производитель'].values[0]).replace("nan","-1"),
         "Страна происхождения":str(similar_tovar[similar_tovar['Id'] == id_]['Страна происхождения'].values[0]).replace("nan","-1"),
         "Вид продукции":str(similar_tovar[similar_tovar['Id'] == id_]['Вид продукции'].values[0]).replace("nan","-1"),
         "Вид товаров":str(similar_tovar[similar_tovar['Id'] == id_]['Вид товаров'].values[0]).replace("nan","-1"),
         "Длина":str(similar_tovar[similar_tovar['Id'] == id_]['Длина'].values[0]).replace("nan","-1"),
         "Ширина":str(similar_tovar[similar_tovar['Id'] == id_]['Ширина'].values[0]).replace("nan","-1"),
         "Высота":str(similar_tovar[similar_tovar['Id'] == id_]['Высота'].values[0]).replace("nan","-1"),
         "Материал":str(similar_tovar[similar_tovar['Id'] == id_]['Материал'].values[0]).replace("nan","-1"),
         "Диаметр":str(similar_tovar[similar_tovar['Id'] == id_]['Диаметр'].values[0]).replace("nan","-1"),
         "Гарантийный срок":str(similar_tovar[similar_tovar['Id'] == id_]['Гарантийный срок'].values[0]).replace("nan","-1"),
         "Цвет":str(similar_tovar[similar_tovar['Id'] == id_]['Цвет'].values[0]).replace("nan","-1"),
         "Вес":str(similar_tovar[similar_tovar['Id'] == id_]['Вес'].values[0]).replace("nan","-1"),
         "Объем":str(similar_tovar[similar_tovar['Id'] == id_]['Объем'].values[0]).replace("nan","-1"),
         "Количество действующих оферт":str(similar_tovar[similar_tovar['Id'] == id_]['Количество действующих оферт'].values[0]).replace("nan","-1"),
         "Сумма в составе контрактов":str(similar_tovar[similar_tovar['Id'] == id_]['Сумма в составе контрактов'].values[0]).replace("nan","-1"),
         "Количество контрактов":str(similar_tovar[similar_tovar['Id'] == id_]['Количество контрактов'].values[0]).replace("nan","-1")})
    print("--- %s seconds ---" % (time.time() - start_time))
    return (similar_tovar_final)

def filters(class_p=None,class_t=None,similar_tovar=None):
    table = pd.DataFrame(pd.Series(similar_tovar[0])).T
    for i in range(1,len(similar_tovar[1:])):
        table.loc[i] = pd.Series(similar_tovar[i])
    if class_p != None:
        table = table[table['Вид продукции'].isin([class_p])]
    elif class_t != None:
        table = table[table['Вид товаров'].isin([class_t])]
    return(table)

def get_similar_tovar_v2(class_p=None,class_t=None,text=None):
    start_time = time.time()
    some = {}
    similar_tovar_id = []
    text_set = get_tags(f'{text}')
    newset = list(data_2['tag_1'])
    data_id = list(data_2['Id'])
    for i in range(len(data_2)):
        try:
            some.update({data_id[i]:len(newset[i] & text_set)})
        except:
            some.update({data_id[i]:0})
    ids = sorted(some.items(),key=operator.itemgetter(1),reverse=True)
    for i in ids:
        if i[1]>0:
            similar_tovar_id.append(i[0])
    #return(data_2['Наименование'][idd])
    similar_tovar = data[data['Id'].isin(similar_tovar_id)]
#     try:
#         similar_tovar = similar_tovar[:100]
#     except:
#         pass
    
    my_class_p = Counter(similar_tovar['Вид продукции'].values)
    my_class_t = Counter(similar_tovar['Вид товаров'].values)
    
    my_class_p = sorted(my_class_p,key=my_class_p.get,reverse=True) 
    try:
        my_class_p = my_class_p[:10]
    except:
        pass
        
    my_class_t = sorted(my_class_t,key=my_class_t.get,reverse=True)
    try:
        my_class_t = my_class_t[:10]
    except:
        pass
    
    
    
    if class_t != None:
        similar_tovar = similar_tovar[similar_tovar['Вид товаров'].isin([class_t])]
    
    elif class_p != None:
        similar_tovar = similar_tovar[similar_tovar['Вид продукции'].isin([class_p])]
    
    return_data = similar_tovar.fillna('-1').to_dict("records")
    
    try:
        return_data = return_data[:50]
    except:
        pass
    
    all_classes = readData()
    
    class_t_p = {}
    for i in my_class_t:
        class_t_p.update({i:[key for key, value in all_classes.items() for letter in [i] if letter in value][0]})
#     if len(return_data) < 2:
#         new_words = []
#         for word in text.split():
#             dataa, code = Sinonims(word)
#             new_words = list(set(new_words) | set(dataa))
#         new_stroke = " ".join(new_words)
#         dataaa = get_similar_tovar_v4(class_p=class_p,class_t=class_t,text=new_stroke)
#         return (dataaa)
    print("--- %s seconds ---" % (time.time() - start_time))
    return({"class_p":my_class_p,"class_t":class_t_p,"payload":return_data})

def get_similar_tovar_v3(class_p=None,class_t=None,texts=None):
    start_time = time.time()
    similar_tovars = []
    newset = list(data_2['tag_1'])
    data_id = list(data_2['Id'])
    j = 0
    for text in texts:
        text_set = get_tags(f'{text}')
        some = {}
        similar_tovar_id = []
        for i in range(len(data_2)):
            try:
                some.update({data_id[i]:len(newset[i] & text_set)})
            except:
                some.update({data_id[i]:0})
        ids = sorted(some.items(),key=operator.itemgetter(1),reverse=True)
        for i in ids:
            if i[1]>0:
                similar_tovar_id.append(i[0])
        #return(data_2['Наименование'][idd])
        similar_tovar = data[data['Id'].isin(similar_tovar_id)][:1]
        similar_tovars.append(similar_tovar.fillna('-1').to_dict("records")[0])
        j += 1
    print("--- %s seconds ---" % (time.time() - start_time))
    return({"payload":similar_tovars})

# def get_similar_tovar_v4(class_p=None,class_t=None,text=None):
#     start_time = time.time()
#     some = {}
#     similar_tovar_id = []
#     text_set = get_tags(f'{text}')
#     newset = list(data_2['tag_1'])
#     data_id = list(data_2['Id'])
#     for i in range(len(data_2)):
#         try:
#             some.update({data_id[i]:len(newset[i] & text_set)})
#         except:
#             some.update({data_id[i]:0})
#     ids = sorted(some.items(),key=operator.itemgetter(1),reverse=True)
#     for i in ids:
#         if i[1]>0:
#             similar_tovar_id.append(i[0])
#     #return(data_2['Наименование'][idd])
#     similar_tovar = data[data['Id'].isin(similar_tovar_id)]
#     my_class_p = Counter(similar_tovar['Вид продукции'].values)
#     my_class_t = Counter(similar_tovar['Вид товаров'].values)
    
#     my_class_p = sorted(my_class_p,key=my_class_p.get,reverse=True)
#     my_class_t = sorted(my_class_t,key=my_class_t.get,reverse=True)
    
#     if class_p != None:
#         similar_tovar = similar_tovar[similar_tovar['Вид продукции'].isin([class_p])]
#     elif class_t != None:
#         similar_tovar = similar_tovar[similar_tovar['Вид товаров'].isin([class_t])]
#     return_data = similar_tovar.fillna('-1').to_dict("records")
#     print("--- %s seconds ---" % (time.time() - start_time))
#     return({"class_p":my_class_p,"class_t":my_class_t,"payload":return_data})


def get_preds(text):
    print(text)
    preds = rules[rules['consequents'].values == frozenset({f'{text}'})]
    a = preds['antecedents'].values
    b = list(map(lambda x: list(x)[0], a))
    print(b)
    return({"preds":b})