import datetime
import re
from time import strftime, localtime
import json
import uuid

LOG_ROOT = 'outputs/'
def csrf_parse(html_doc):
    with open(LOG_ROOT+"csrf_parse.html", "w") as res:
        res.write(html_doc)
    match = re.search(r"\'csrf_token\':\s*\"(\w+)\"", html_doc)
    if match:
        csrf_token = match.group(1)
        return csrf_token
    else:
        raise ValueError("CSRF token not found in the HTML document.")



def user_parse(html_doc):
    with open("user_parse.html", "w") as res:
        res.write(html_doc)
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
    if type(agenda) == str :
        agendaObject = json.loads(agenda)
    dayArray = agendaObject['jours']
    itemsArray = agendaObject['items']
    print(dayArray)
    print(itemsArray)

    formattedDayArray = []
    formattedItemArray = []

    for day in dayArray:
        formattedDay = {}
        formattedDay['type'] = agendaTypeLUT[day['type']]
        formattedDay['dayNum'] = day['jour']
        formattedDay['date'] = epoch_to_str(day['date']/1000) # strftime('%Y-%m-%d %H:%M:%S', localtime(day['date']/1000))
        formattedDayArray.append(formattedDay)
        print(formattedDay)

    for item in itemsArray:
        formattedItem = {}
        formattedItem['day'] = epoch_to_str(get_day_of_epoch(item['debut']))
        formattedItem['begin'] = epoch_to_str(item['debut']/1000)
        formattedItem['end'] = epoch_to_str(item['fin']/1000)
        formattedItem['title'] = item['titre']
        formattedItem['id'] = item['idItem']
        formattedItem['data'] = json.loads(item['data'])
        formattedItemArray.append(formattedItem)
        print(formattedItem)


def get_day_of_epoch(epoch):
    dateObject = datetime.datetime.fromtimestamp(epoch/1000)
    day = dateObject.date()
    return datetime.datetime(year=day.year, month=day.month, day=day.day).timestamp()

def epoch_to_str(epoch):
    return strftime('%Y-%m-%d %H:%M:%S', localtime(epoch))
