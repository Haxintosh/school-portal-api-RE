import datetime
import time

import bcolors
import re
from time import strftime, localtime
import json
import uuid
from bs4 import BeautifulSoup

import api


class Course:
    def __init__(self, subject, day, start, end, teacher, location, id):
        self.subject = subject
        self.day = day
        self.start = start
        self.end = end
        self.teacher = teacher
        self.location = location
        self.tasks = []
        self.id = id
    def __str__(self):
        return f"Subject: {self.subject}\nDay: {self.day}\nStart: {self.start}\nEnd: {self.end}\nTeacher: {self.teacher}\nLocation: {self.location}\nTasks: {self.tasks}\nID: {self.id}"


class Day:
    def __init__(self, date, dayNum, type):
        self.dayNum = dayNum
        self.date = date
        self.type = type
        self.courses = []
    def __str__(self):
        return f"Day: {self.dayNum}\nDate: {self.date}\nType: {self.type}\nCourses: {self.courses}"

LOG_ROOT = 'outputs/'
def csrf_parse(html_doc):
    match = re.search(r"\'csrf_token\':\s*\"(\w+)\"", html_doc)
    if match:
        csrf_token = match.group(1)
        return csrf_token
    else:
        raise ValueError("CSRF token not found in the HTML document.")

def user_parse(html_doc):
    match = re.search(r"const typesUsager = \[(.*)\];", html_doc)
    if match:
        user_list = match.group(1)
        return user_list
    else:
        raise ValueError("User list not found in the HTML document.")

def get_requete_usager(typeUsager):
    typeUsagerList = {
        "type": typeUsager.get("type"),
        "typeNum1": typeUsager.get("typeNum1"),
        "typeNum2": typeUsager.get("typeNum2"),
        "typeNum3": typeUsager.get("typeNum3")
    }
    return typeUsagerList

def get_typeUsager(typeUsagers):
    typeUsager = "[" + typeUsagers.replace("},{", "},{") + "]"
    data = json.loads(typeUsager)
    res = data[1]
    return res

def gen_srv_json_payload(leModule, operation, typeUsager, data):
    requetes = {
        "id" : str(uuid.uuid4()),
        "leModule" : leModule,
        "operation" : operation,
        "typeUsager": typeUsager,
        "data": data
    }
    data_payload = {
        "id" : str(uuid.uuid4()),
        "requetes" : [requetes]
    }

    return_payload = f"data={json.dumps(data_payload, separators=(',', ':'))}"
    return return_payload

def parseAgenda(agenda):
    agendaTypeLUT = {
        0 : 'school',
        80 : 'pedagogical'
    }

    agendaObject = None
        # sample: {"jours":[{"type":0,"jour":"Jour 3","date":1695009600000},{"type":0,"jour":"Jour 4","date":1695096000000},{"type":0,"jour":"Jour 5","date":1695182400000},{"type":0,"jour":"Jour 6","date":1695268800000},{"type":80,"jour":"Journée pédag.","date":1695355200000}],"items":[{"type":1,"debut":1695230700000,"fin":1695235200000,"titre":"Anglais","idItem":"2023-501-ANGR404    -04   -1-00006","data":"{\"noCours\":6,\"aNote\":false,\"aDiscussion\":false,\"nomLong\":\"Anglais\",\"enseignant\":\"Feuiltault, Jessica\",\"local\":\"286\",\"ecole\":\"501\",\"lignes\":[{\"aNote\":false,\"aDiscussion\":false,\"type\":1,\"icone\":0,\"aEcheance\":false,\"fichiersARemettre\":false,\"idItem\":\"2023-501-ANGR404    -04   -1-0000000004\",\"titre\":\"Cours #5-9- The Butterfly Effect (See Google Classroom)\"},{\"aNote\":false,\"aDiscussion\":false,\"type\":2,\"icone\":5,\"aEcheance\":true,\"fichiersARemettre\":false,\"idItem\":\"2023-501-ANGR404    -04   -1-01-0-002\",\"titre\":\"Grammar Test #1\"}]}","couleur":"#d16fac","couleurCustom":""},{"type":1,"debut":1695225900000,"fin":1695230400000,"titre":"Arts","idItem":"2023-501-ART402     -04   -1-00003","data":"{\"noCours\":3,\"aNote\":false,\"aDiscussion\":false,\"nomLong\":\"Arts\",\"enseignant\":\"Fournier-Hébert, Mathilde\",\"local\":\"298\",\"ecole\":\"501\",\"lignes\":[{\"aNote\":false,\"aDiscussion\":false,\"type\":2,\"icone\":11,\"aEcheance\":false,\"fichiersARemettre\":false,\"idItem\":\"2023-501-ART402     -04   -1-01-0-001\",\"titre\":\"Remise de la photo originale de la blessure + photo modifiée\"},{\"aNote\":false,\"aDiscussion\":false,\"type\":2,\"icone\":11,\"aEcheance\":false,\"fichiersARemettre\":false,\"idItem\":\"2023-501-ART402     -04   -1-01-0-002\",\"titre\":\"Montage final du projet fausse blessure\"},{\"aNote\":false,\"aDiscussion\":false,\"type\":2,\"icone\":0,\"aEcheance\":false,\"fichiersARemettre\":false,\"idItem\":\"2023-501-ART402     -04   -1-02-0-001\",\"titre\":\"Appréciation critique\"},{\"aNote\":false,\"aDiscussion\":false,\"type\":2,\"icone\":11,\"aEcheance\":false,\"fichiersARemettre\":false,\"idItem\":\"2023-501-ART402     -04   -1-01-1-001\",\"titre\":\"Remise du scénario\"}]}","couleur":"#ff6699","couleurCustom":""},{"type":1,"debut":1695144300000,"fin":1695148800000,"titre":"CCQ","idItem":"2023-501-CCQ404     -04   -1-00003","data":"{\"noCours\":3,\"aNote\":false,\"aDiscussion\":false,\"nomLong\":\"CCQ\",\"enseignant\":\"St-Louis, Marc\",\"local\":\"B-205\",\"ecole\":\"501\",\"lignes\":[]}","couleur":"","couleurCustom":""},{"type":1,"debut":1695048300000,"fin":1695052800000,"titre":"Éd. physique-santé","idItem":"2023-501-EDPS402    -04   -1-00003","data":"{\"noCours\":3,\"aNote\":false,\"aDiscussion\":false,\"nomLong\":\"Éd. physique-santé\",\"enseignant\":\"St-Germain, Viviane\",\"local\":\"GYM\",\"ecole\":\"501\",\"lignes\":[]}","couleur":"#b53f41","couleurCustom":""},{"type":1,"debut":1695038700000,"fin":1695043200000,"titre":"Français","idItem":"2023-501-FRA406     -04   -1-00008","data":"{\"noCours\":8,\"aNote\":false,\"aDiscussion\":false,\"nomLong\":\"Français\",\"enseignant\":\"Rodi, Mellissa\",\"local\":\"B-207\",\"ecole\":\"501\",\"lignes\":[{\"aNote\":false,\"aDiscussion\":false,\"type\":2,\"icone\":3,\"aEcheance\":true,\"fichiersARemettre\":false,\"idItem\":\"2023-501-FRA406     -04   -1-01-1-003\",\"titre\":\"Notes de cours (auteur + contextualisation)\"},{\"aNote\":false,\"aDiscussion\":false,\"type\":2,\"icone\":3,\"aEcheance\":false,\"fichiersARemettre\":false,\"idItem\":\"2023-501-FRA406     -04   -1-01-1-004\",\"titre\":\"Classes de mots + « Incendies »\"}]}","couleur":"#57b2d4","couleurCustom":""},{"type":1,"debut":1695211500000,"fin":1695216000000,"titre":"Français","idItem":"2023-501-FRA406     -04   -1-00009","data":"{\"noCours\":9,\"aNote\":false,\"aDiscussion\":false,\"nomLong\":\"Français\",\"enseignant\":\"Rodi, Mellissa\",\"local\":\"B-207\",\"ecole\":\"501\",\"lignes\":[{\"aNote\":false,\"aDiscussion\":false,\"type\":2,\"icone\":3,\"aEcheance\":true,\"fichiersARemettre\":false,\"idItem\":\"2023-501-FRA406     -04   -1-01-1-004\",\"titre\":\"Classes de mots + « Incendies »\"},{\"aNote\":false,\"aDiscussion\":false,\"type\":2,\"icone\":3,\"aEcheance\":false,\"fichiersARemettre\":false,\"idItem\":\"2023-501-FRA406     -04   -1-01-1-005\",\"titre\":\"Groupes de mots + « Incendies »\"}]}","couleur":"#57b2d4","couleurCustom":""},{"type":1,"debut":1695302700000,"fin":1695307200000,"titre":"Français","idItem":"2023-501-FRA406     -04   -1-00010","data":"{\"noCours\":10,\"aNote\":false,\"aDiscussion\":false,\"nomLong\":\"Français\",\"enseignant\":\"Rodi, Mellissa\",\"local\":\"B-312\",\"ecole\":\"501\",\"lignes\":[{\"aNote\":false,\"aDiscussion\":false,\"type\":2,\"icone\":3,\"aEcheance\":false,\"fichiersARemettre\":false,\"idItem\":\"2023-501-FRA406     -04   -1-01-1-005\",\"titre\":\"Groupes de mots + « Incendies »\"}]}","couleur":"#57b2d4","couleurCustom":""},{"type":1,"debut":1695125100000,"fin":1695129600000,"titre":"Histoire","idItem":"2023-501-HIS404     -04   -1-00007","data":"{\"noCours\":7,\"aNote\":false,\"aDiscussion\":false,\"nomLong\":\"Histoire\",\"enseignant\":\"Guimond, Patricia\",\"local\":\"B-206\",\"ecole\":\"501\",\"lignes\":[]}","couleur":"","couleurCustom":""},{"type":1,"debut":1695317100000,"fin":1695321600000,"titre":"Histoire","idItem":"2023-501-HIS404     -04   -1-00008","data":"{\"noCours\":8,\"aNote\":false,\"aDiscussion\":false,\"nomLong\":\"Histoire\",\"enseignant\":\"Guimond, Patricia\",\"local\":\"286\",\"ecole\":\"501\",\"lignes\":[]}","couleur":"","couleurCustom":""},{"type":1,"debut":1695057900000,"fin":1695062400000,"titre":"Math-SN","idItem":"2023-501-MATSN406   -04   -1-00008","data":"{\"noCours\":8,\"aNote\":false,\"aDiscussion\":false,\"nomLong\":\"Math-SN\",\"enseignant\":\"Rouleau, Étienne\",\"local\":\"B-306\",\"ecole\":\"501\",\"lignes\":[{\"aNote\":false,\"aDiscussion\":false,\"type\":1,\"icone\":0,\"aEcheance\":false,\"fichiersARemettre\":false,\"idItem\":\"2023-501-MATSN406   -04   -1-0000000009\",\"titre\":\"2.1.1 La double mise en évidence\"}]}","couleur":"#7d5dc1","couleurCustom":""},{"type":1,"debut":1695129900000,"fin":1695134400000,"titre":"Math-SN","idItem":"2023-501-MATSN406   -04   -1-00009","data":"{\"noCours\":9,\"aNote\":false,\"aDiscussion\":false,\"nomLong\":\"Math-SN\",\"enseignant\":\"Rouleau, Étienne\",\"local\":\"B-306\",\"ecole\":\"501\",\"lignes\":[{\"aNote\":false,\"aDiscussion\":false,\"type\":1,\"icone\":0,\"aEcheance\":false,\"fichiersARemettre\":false,\"idItem\":\"2023-501-MATSN406   -04   -1-0000000010\",\"titre\":\"2.1.3 La méthode produit-somme\"}]}","couleur":"#7d5dc1","couleurCustom":""},{"type":1,"debut":1695216300000,"fin":1695220800000,"titre":"Math-SN","idItem":"2023-501-MATSN406   -04   -1-00010","data":"{\"noCours\":10,\"aNote\":false,\"aDiscussion\":false,\"nomLong\":\"Math-SN\",\"enseignant\":\"Rouleau, Étienne\",\"local\":\"B-306\",\"ecole\":\"501\",\"lignes\":[{\"aNote\":false,\"aDiscussion\":false,\"type\":1,\"icone\":0,\"aEcheance\":false,\"fichiersARemettre\":false,\"idItem\":\"2023-501-MATSN406   -04   -1-0000000011\",\"titre\":\"Résolution de problèmes\"},{\"aNote\":false,\"aDiscussion\":false,\"type\":2,\"icone\":5,\"aEcheance\":true,\"fichiersARemettre\":false,\"idItem\":\"2023-501-MATSN406   -04   -1-01-0-005\",\"titre\":\"Situation-problème : De l'ordre sur l'affiche\"}]}","couleur":"#7d5dc1","couleurCustom":""},{"type":1,"debut":1695297900000,"fin":1695302400000,"titre":"Math-SN","idItem":"2023-501-MATSN406   -04   -1-00011","data":"{\"noCours\":11,\"aNote\":false,\"aDiscussion\":false,\"nomLong\":\"Math-SN\",\"enseignant\":\"Rouleau, Étienne\",\"local\":\"B-306\",\"ecole\":\"501\",\"lignes\":[{\"aNote\":false,\"aDiscussion\":false,\"type\":1,\"icone\":0,\"aEcheance\":false,\"fichiersARemettre\":false,\"idItem\":\"2023-501-MATSN406   -04   -1-0000000012\",\"titre\":\"2.2 La factorisation à l'aide des identités algébriques\"}]}","couleur":"#7d5dc1","couleurCustom":""},{"type":1,"debut":1695043500000,"fin":1695048000000,"titre":"Sc. et techn.","idItem":"2023-501-SCT404     -04   -1-00008","data":"{\"noCours\":8,\"aNote\":false,\"aDiscussion\":false,\"nomLong\":\"Sc. et techn.\",\"enseignant\":\"Thériault, Valérie\",\"local\":\"294\",\"ecole\":\"501\",\"lignes\":[{\"aNote\":false,\"aDiscussion\":false,\"type\":1,\"icone\":0,\"aEcheance\":false,\"fichiersARemettre\":false,\"idItem\":\"2023-501-SCT404     -04   -1-0000000001\",\"titre\":\"Chapitre 1 : L'atome de Carbone\"}]}","couleur":"#d16d50","couleurCustom":""},{"type":1,"debut":1695134700000,"fin":1695139200000,"titre":"Sc. et techn.","idItem":"2023-501-SCT404     -04   -1-00009","data":"{\"noCours\":9,\"aNote\":false,\"aDiscussion\":false,\"nomLong\":\"Sc. et techn.\",\"enseignant\":\"Thériault, Valérie\",\"local\":\"222\",\"ecole\":\"501\",\"lignes\":[{\"aNote\":false,\"aDiscussion\":false,\"type\":1,\"icone\":0,\"aEcheance\":false,\"fichiersARemettre\":false,\"idItem\":\"2023-501-SCT404     -04   -1-0000000002\",\"titre\":\"Chapitre 2 : L'agriculture hors-sol\"}]}","couleur":"#d16d50","couleurCustom":""},{"type":1,"debut":1695312300000,"fin":1695316800000,"titre":"Sc. et techn.","idItem":"2023-501-SCT404     -04   -1-00010","data":"{\"noCours\":10,\"aNote\":false,\"aDiscussion\":false,\"nomLong\":\"Sc. et techn.\",\"enseignant\":\"Thériault, Valérie\",\"local\":\"222\",\"ecole\":\"501\",\"lignes\":[{\"aNote\":false,\"aDiscussion\":false,\"type\":1,\"icone\":0,\"aEcheance\":false,\"fichiersARemettre\":false,\"idItem\":\"2023-501-SCT404     -04   -1-0000000002\",\"titre\":\"Chapitre 2 : L'agriculture hors-sol\"}]}","couleur":"#d16d50","couleurCustom":""}]}
    if type(agenda) == str:
        agendaObject = json.loads(agenda)
    dayArray = agendaObject['jours']
    itemsArray = agendaObject['items']

    formattedDayArray = []
    formattedItemArray = []

    for day in dayArray:
        currentDay = Day(date=day['date']/1000, dayNum=day['jour'], type=day['type'])
        formattedDayArray.append(currentDay)

        api.log.write('CALENDAR - DAYS'+'\n')
        # for debug purposes
        formattedDay = {}
        formattedDay['type'] = agendaTypeLUT[day['type']]
        formattedDay['dayNum'] = day['jour']
        formattedDay['date'] = epoch_to_str(
            day['date'] / 1000)  # strftime('%Y-%m-%d %H:%M:%S', localtime(day['date']/1000))
        api.log.write(str(formattedDay)+'\n')

    for item in itemsArray:
        courseData = json.loads(item['data'])
        currentCourse = Course(subject= item['titre'], day=get_day_of_epoch(item['debut']), start=item['debut']/1000, end=item['fin']/1000, teacher=courseData['enseignant'], location=courseData['local'], id=item['idItem'])
        formattedItemArray.append(currentCourse)
        for i in courseData['lignes']:
            task = {}
            task['title'] = i['titre']
            task['type'] = i['type']
            task['typeV2'] = i['icone']
            task['isGraded'] = i['aNote']
            task['isDue'] = i['aEcheance']
            task['submittable'] = i['fichiersARemettre']
            currentCourse.tasks.append(task)

        api.log.write('CALENDAR - COURSES'+'\n')
        # for debug purposes
        formattedItem = {}
        formattedItem['day'] = epoch_to_str(get_day_of_epoch(item['debut']))
        formattedItem['begin'] = epoch_to_str(item['debut'] / 1000)
        formattedItem['end'] = epoch_to_str(item['fin'] / 1000)
        formattedItem['title'] = item['titre']
        formattedItem['id'] = item['idItem']
        formattedItem['data'] = json.loads(item['data'])
        api.log.write(str(formattedItem)+'\n')

    for i in formattedItemArray:
        for j in formattedDayArray:
            if round(i.day) == round(j.date):
                j.courses.append(i)

    for i in formattedDayArray:
        print(i.__str__(), '\n')


def parseGrades(html):
    soup = BeautifulSoup(html, features="html.parser")
    matching_tags = soup.find_all('option')
    coursesList = []
    coursesIDs = []
    for i in matching_tags:
        if i['value'].startswith('Travaux.srf?Detail=O'):
            print(i.text.strip())
            coursesList.append(i.text.strip())
            matches = re.findall(r'\[(.*)-', string=i.text.strip())
            if matches:
                coursesIDs.append(matches[0])

    exams = []
    examElements = soup.find_all('tbody')
    for i in examElements:
        currentExam = []
        nobr = i('nobr')
        for j in nobr:
            if j.text:
                if j.text.find('|') != -1:
                    split = cleanString(j.text.strip())
                    currentExam.append(split[0])
                    currentExam.append(split[1])
                else:
                    currentExam.append(j.text.strip())
        span = i('span')
        # get data
        for k in span:
            try:
                if k['pluri-params']:
                    currentExam.append(json.loads(k['pluri-params']))
                    # currentExam.append('SKIP')
            except any as e:
                pass

        td = i('td')
        for l in td:
            if l.text.strip():
                try:
                    if l['align']:
                        currentExam.append(l.text.strip())
                except (KeyError) as e:
                    pass
        exams.append(currentExam)
    exams = [sub for sub in exams if sub]
    return formatExams(exams)

def get_day_of_epoch(epoch):
    dateObject = datetime.datetime.fromtimestamp(epoch/1000)
    day = dateObject.date()
    return datetime.datetime(year=day.year, month=day.month, day=day.day).timestamp()

def epoch_to_str(epoch):
    return strftime('%Y-%m-%d %H:%M:%S', localtime(epoch))

def prettifyHTML(html, name):
    soup = BeautifulSoup(html, 'html.parser')
    f = open(f'outputs/{name}.html', 'w')
    f.write(soup.prettify())
    f.close()

def cleanString(string):
    if string.find('|') != -1:
        split = string.split('|')
        returnArray = []
        for i in split:
            returnArray.append(i.replace('\r\n', ' ').strip())
        return returnArray
    else:
        return None
def formatExams(exams):
    positionMap ={
        0:'date',
        1:'type',
        2:'name',
        3:'data',
        4:'competency',
        5:'weight',
        6:'maxRes',
        7:'res',
        8:'resPercent'
    }

    returnArray = []

    for i in exams:
        currentExam = {}
        for index, e in enumerate(i):
            currentExam[positionMap[index]] = e
        returnArray.append(currentExam)
    print(returnArray)
    return returnArray

# def parseMessages(html):
#     start_time = time.time()
#     positionMap = {
#         0:'sender',
#         1:'title',
#         2:'time',
#         3:'receiver',
#         4:'id'
#     }
#     msg_id_regex = re.compile(r"CourrielDetail.srf\?IDCourriel=([^')]*)")
#
#     soup = BeautifulSoup(html, 'html.parser')
#     message_elements = soup.find_all('tr', class_='PointeurMain')
#     unformatted_messages = []
#     for i in message_elements:
#         inner_html = i.text.strip()
#         href = i('a')
#         if href:
#             href = re.findall(msg_id_regex, href[0]['href'])
#             if href:
#                 inner_html += f'\n{href[0]}'
#         unformatted_messages.append(inner_html)
#     formatted_messages = []
#     for j in unformatted_messages:
#         single_message = j.split('\n')
#         current_message = {}
#         for index, k in enumerate(single_message):
#             current_message[positionMap[index]] = k
#         formatted_messages.append(current_message)
#     print(formatted_messages)
#     print(f'Eexecution took {time.time()-start_time}') # what it's 0.03 or 0.07
#     return formatted_messages

def parseMessages(html):
    positionMap = {
        0: 'sender',
        1: 'title',
        2: 'time',
        3: 'receiver',
        4: 'id'
    }
    msg_id_regex = re.compile(r"CourrielDetail.srf\?IDCourriel=([^')]*)")

    soup = BeautifulSoup(html, 'html.parser')
    message_elements = soup.find_all('tr', class_='PointeurMain')
    formatted_messages = []
    if not message_elements:
        bcolors.Logging.error(thread="parse/messages", error="No message elements found!")
        return
    for element in message_elements:
        message_data = [text.strip() for text in element.stripped_strings]
        href = element.find('a', href=True)
        if href:
            match = msg_id_regex.search(href['href'])
            if match:
                message_data.append(match.group(1))

        message_dict = {positionMap[index]: value for index, value in enumerate(message_data) if index in positionMap}
        formatted_messages.append(message_dict)

    print(formatted_messages)
    return formatted_messages

def parseSingleMessage(html):
    main_msg = {}
    soup = BeautifulSoup(html, 'html.parser')
    main_msg_elements = soup('tbody')
    main_msg['message'] = main_msg_elements[1].text.strip().replace(u'\xa0', u' ')

    attached_files = []
    for i in main_msg_elements[0]('a'):
        if i['href'].startswith('javascript:'):
            continue

        current_file = {}
        current_file['name'] = i.text.strip()
        current_file['link'] = i['href']
        attached_files.append(current_file)

    main_msg['files'] = attached_files

    positionMap = {
        "subject" : "Objet :\n",
        "from" : "De :\n",
        "to" : "À :\n",
        "date" : "Date :\n"
    }
    for j in main_msg_elements[0]('tr'):
        for k in positionMap:
            if j.text.strip().startswith(positionMap[k]):
                main_msg[k] = j.text.strip().removeprefix(positionMap[k])
    print(main_msg)
    return main_msg

def time_it(function):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = function(*args, **kwargs)
        print(f"{function.__name__} execution took {round(time.time()-start_time, 4)}s")
        return res
    return wrapper