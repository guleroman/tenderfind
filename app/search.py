import re
import os
import json
from collections import Counter
import pandas as pd
import pymorphy2
import operator
import time
#from recognition_themes2 import moodDetection 
from speller import Speller 
morph = pymorphy2.MorphAnalyzer()

global data
data = pd.read_excel('../test_data/data.xlsx')

global data_2
data_2 = pd.read_pickle('../test_data/data_tag_1.pkl')

listt = ('''которых которые твой которой которого сих ком свой твоя этими слишком нами всему будь саму чаще ваше сами наш затем
каждая также чему собой самими нем вами ими откуда такие тому та очень сама нему алло оно этому кому тобой таки твоё
каждые твои мой нею самим ваши ваша кем мои однако сразу свое ними всё неё тех хотя всем тобою тебе одной другие
этао само эта буду самой моё своей всею будут своего кого свои мог нам особенно её самому наше кроме вообще вон
мною никто это и в во не что он на я с со как а то все она так его но да ты к у же вы за бы по только ее мне было вот от меня еще нет 
о из ему теперь когда даже ну вдруг ли если уже или ни быть был него до вас нибудь опять уж вам ведь там потом себя ничего ей может они тут где есть надо ней
для мы тебя их чем была сам чтоб без будто чего раз тоже себе под будет ж тогда кто этот того потому этого какой совсем ним здесь этом один почти мой тем чтобы 
нее сейчас были куда зачем всех никогда можно при наконец два об другой хоть после над больше тот через эти нас про всего них какая много разве три эту 
моя впрочем свою этой перед иногда лучше чуть том нельзя им более всегда конечно всю между  россия санкт бразилия индия калифорния канада йорк техас 
виктория елена колумбия франция александр сергей ирина ольга татьяна флорида италия андрей киев аргентина каролина наталья светлана стамбул лондон алексей 
владимир дмитрий паулу франс вашингтон анастасия анна галина екатерина людмила марина мария оксана юлия одесса  евгений иван игорь максим николай олег париж 
алена алёна армения валентина вирджиния надежда саша алания аризона голландия дима ирландия рома самара сидней уфа хьюстон антон артем артём виктор денис израиль 
михаил павел роман юрий торонто чили никита александра евгения кристина илья индиана руслан алина виталий настя дели джерси канзас любовь альберта мельбурн санта 
лариса барселона дагестан катя дания теннесси дарья наташа ксения уэст вадим кирилл наталия влад университета оля луис анатолий диего алма константин эмилия рейн 
аня василий юля иран вера нина яна ивано кентукки иванов женя милан невада вячеслав таня инна макс остин кения юта артур валерия минас олеся диана валерий атланта 
берлин марий владислав алла ленина саха маша леон даша тула вегас улан егор данил бостон полина душанбе орел юра чита корпус лилия колумбус валенсия карина вероника 
света орландо сантьяго миша карелия тамара азия вика вова ваня саня маргарита баден серёга вася антонио фрунзе гранд даллас катерина коля петр пётр лена европа
 елизавета костя коста тимур род лима геннадий филадельфия житомир жанна станислав даниил кинг лидия лиза ола осло александрия кострома ричмонд стас сербия лагос
  ксюша белая валера анюта эдуард слава шри ангелина рика борис айленд леонид паша алиса дакота рига проф лера майне ниу богдан севилья солт альбина сальвадор 
  ярослав манила армавир каир ланка софия ира марат бали рим химико леха лёха петра эльвира питер анжелика катарина рустам эссекс кали рок мир григорий сицилия 
  алекс энгельс натали георгий арина дублин алтай дурбан надя панама сомерсет дел бай кент валентин аделаида ран франко таллин анжела мэн зам антонина семен семён 
  там фёдор кипр федор доминго санто тринидад виталик монтана катюша кызыл детройт роза женева ника зоя кузьмина люба милано дела ринат раиса девон жека крус 
  салават ульяна адана кира леша лёша измит степан лида юрист оман хилл соня софья златоуст али аленка алёнка дина нор бруклин худ рона хуан альберт денвер витя
   айгуль джексон авто динара джамбул куба леся регина люда абик гульнара ивана линкольн оксфорд уинстон галя герцена мадина труда сьерра азамат олександр кале
    тобаго валя боливар сережа серёжа настёна дейтон венеция настена глеб брайтон никитин алия муз ильина рита эльмира салвадор салон давид тёма норт данила мемфис 
    ширак алеся ярослава катюшка мерида батон грин ева джалал кота лестер абу марк дорсет рочестер виолетта айдын дамир димон толедо марта бар мед кас лара влада лори
     арсен елец кингстон зинаида абад ида лиля аль володимир снежана феодосия даня измаил дус петя римма мади арт бэй милана мира элина матвей мид лев назар тарас берк 
     веллингтон мороз оленька мак омаха майя мила кара володя джамби лансинг ася ишим бреда кут спринг шаркия ген айгерим албания даля зарина инга герман уэйн барбара
      аркадий рамиль виталя милтон ангел мами авив тимофей пол дарина бихар доцент венера лина ами анечка бат олечка байконур ислам магомед абердин шамиль светик маврикий
       лёв лонг честер амина арман астурия верона василиса иванович юджин альфия илона маришка саванна лис танка бей сашка шах айнур лиана аслан банда йемен кунгур артема
        гузель мировой кан роли алевтина элизабет ван славик гамильтон варвара наталя нелли гуля фото белен вена сабах король балта джордан эдик асель рай энн арсений бари 
        жуан лион дана марианна сабина беверли лагуна меса росарио бенд берген крит мат аврора аида пальма ривер шуя аксай апу алмаз алсу милена витория мэдисон василь гай 
        волк инта клауд адм айдар алик гриша мурат анализа армия джулия гена светлый ренат берн сонора хайфа карлос ливия флоренция хана юлька радик дерби жозе юго гульназ 
        клара кристи лейла савина андрюха булган гран сидар так тур вита эля дашка миха сала лана олька смела азат алишер данияр джон дон строй хай айдана камила моника канта владик 
        нурлан эльдар гора пушкин сер аля ларина настенька поляна тюбе арарат педро роберт толик мари ден рафаэль серый таисия маркса юленька или миллер инесса руслана алам монтгомери
        мирослава самая фатима ната сток вида лика агна амир мурад ростислав баки вован тура уэй медина союза сурат захар микола святослав зульфия луиза толя физа адам ильяс султан 
        димка нова оби серик акад аллен рустем вас женечка лоуренс море серж стерлинг токмак фарфор милашка генуя мага ник саф аллах ахмед дар марсель комо фалькон анталия лада маруся
         олена викуся саки сафа абай восток федя айжан неля элла мун гоша кирил яков беркли чарльз альфа иринка алиночка кашмир ярик айрат армен кулик маркс петро расул родион эмиль брага
          ванёк величко виндзор тулун гульмира маринка юлиана дашуля зима булат ерлан ибрагим саид джордж ильнур престон сухой фарго алеша''').split(' ')

global stop_words
stop_words = Counter(listt)

def stopfuckingwords(words, stop_words):
    return (list(Counter(words) - stop_words))

def text_preprocess(text):
    text = text.lower()
    ll = re.findall(r'\w+', text) # Разбивка строки на слова, без учета знаков препинания.
    ls = [morph.parse(word)[0].normal_form for word in ll if len(word) >= 3] # Приведение слов, длина которых >= 3  к нормальной форме
    ls = stopfuckingwords(ls,stop_words)
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
    my_class_p = Counter(similar_tovar['Вид продукции'].values)
    my_class_t = Counter(similar_tovar['Вид товаров'].values)
    
    my_class_p = sorted(my_class_p,key=my_class_p.get,reverse=True)
    my_class_t = sorted(my_class_t,key=my_class_t.get,reverse=True)
    
    if class_p != None:
        similar_tovar = similar_tovar[similar_tovar['Вид продукции'].isin([class_p])]
    elif class_t != None:
        similar_tovar = similar_tovar[similar_tovar['Вид товаров'].isin([class_t])]
    print("--- %s seconds ---" % (time.time() - start_time))
    return({"class_p":my_class_p,"class_t":my_class_t,"payload":similar_tovar.fillna('-1').to_dict("records")})