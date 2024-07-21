from utils import *
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
import time
import datetime
import bcolors
import requests

login_url = 'https://portail.cje.qc.ca/pluriportail/pfr/LoginReq.srf?Etape=2&Login=1'
main_srf_url = 'https://portail.cje.qc.ca/pluriportail/pfr/Main.srf?ProfilType=1&Nav=OUI'
rest_api_key_url = 'https://portail.cje.qc.ca/pluriportail/ServeurJSON.srf?M1-OP14~'
logout_url = 'https://portail.cje.qc.ca/pluriportail/pfr/Logout.srf'
agenda_url = 'https://portail.cje.qc.ca/pluriportail/pfr/Agenda.srf'

LOG_ROOT = 'outputs/'

# TODO 1. Error handling, 2. Agenda parsing

log = open(LOG_ROOT+datetime.datetime.now().strftime('%H:%M:%S')+'.log', 'a')
log.write(f"""
Portal log file on {datetime.datetime.now().strftime('%H:%M:%S')}\n
""")

login_header = {
    'User-Agents' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148' ,
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://portail.cje.qc.ca",
    "DNT": "1",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "same-origin",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}

main_srf_header = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 ",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,/;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}

def login(username, password):
    login_payload = {
        'NomLogin': username,
        'IDEcoleOpenID': "{{+IDEcoleOpenID}}",
        'MotPasse': password,
        'ChargeLaPage': 'F01'
    }

    session = requests.session()
    session.cookies.clear()


    # <----- LOGIN ----->
    bcolors.Logging.info(thread="session/login/login", error="Sending login payload")
    login = session.post(url=login_url, headers=login_header, data=login_payload)
    log.write("SESSION LOGIN STATUS: " + str(login.status_code) + '\n')
    log.write("SESSION LOGIN COOKIES: " + str(login.cookies) + '\n')
    log.write("SESSION LOGIN HEADER: " + str(login.headers) + '\n')
    log.write("SESSION LOGIN TXT: " + str(login.text) + '\n\n')



    # <----- CSRF ----->
    global csrf_token

    bcolors.Logging.info(thread="session/login/csrf", error="Sending CSRF (main.srf) payload")
    main_srf = session.get(url=main_srf_url, headers=main_srf_header)
    csrf_token = csrf_parse(html_doc=main_srf.text)
    log.write("SESSION CSRF STATUS: " + str(main_srf.status_code) + '\n')
    log.write("SESSION CSRF COOKIES: " + str(main_srf.cookies) + '\n')
    log.write("SESSION CSRF HEADER: " + str(main_srf.headers) + '\n')
    log.write("SESSION CSRF TXT: " + str(main_srf.text) + '\n\n')

    rest_api_key_header = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'X-PluriToken': csrf_token,
        'X-Requested-With': 'XMLHttpRequest',
        'Host': 'portail.cje.qc.ca',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://portail.cje.qc.ca/pluriportail/pfr/Main.srf?ProfilType=1&Nav=OUI',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }

    # <----- FILLER ----->
    bcolors.Logging.info(thread="session/login/filler", error="Sending filler payloads")
    session.get(url=f"https://portail.cje.qc.ca/pluriportail/pfr/MenuPrincipal.srf?_={round(time.time())}", headers=rest_api_key_header)


    # <----- TIMER ----->
    bcolors.Logging.info(thread="session/login/timer", error="Sending session timer payload (INIT!)")

    timer_session = session.get(
        url=f"https://portail.cje.qc.ca/pluriportail/pfr/TimerSess.srf?Timer=OUI&_={round(time.time())}",
        headers=rest_api_key_header)

    log.write("SESSION TIMER STATUS: " + str(timer_session.status_code) + '\n')
    log.write("SESSION TIMER COOKIES: " + str(timer_session.cookies) + '\n')
    log.write("SESSION TIMER HEADER: " + str(timer_session.headers) + '\n')
    log.write("SESSION TIMER TXT: " + str(timer_session.text) + '\n')

    bcolors.Logging.info(thread="session/login/filler", error="Sending post timer filler payloads")
    session.get(url=f"https://portail.cje.qc.ca/pluriportail/pfr/ProfilType.srf?Bidon=1&Nav=OUI&ChargeLaPage=F00&_={round(time.time())}", headers=rest_api_key_header)

    session.get(url="https://portail.cje.qc.ca/pluriportail/pfr/Main.srf?MainAccueil=1", headers=rest_api_key_header)

    session.get(url=f"https://portail.cje.qc.ca/pluriportail/pfr/MenuPrincipal.srf?_={round(time.time())}", headers=rest_api_key_header)

    # <----- RESTAPI KEY ----->
    bcolors.Logging.info(thread="session/login/restapi", error="Sending REST API KEY payload")
    rest_api_key_payload = gen_srv_json_payload(operation=14, data=None, leModule=1, typeUsager=get_requete_usager(get_typeUsager(user_parse(main_srf.text))))
    rest_api_key = session.post(url=rest_api_key_url, headers=rest_api_key_header, data=rest_api_key_payload)
    log.write("SESSION RESTAPI KEY GET STATUS: " + str(rest_api_key.status_code) + '\n')
    log.write("SESSION RESTAPI KEY GET COOKIES: " + str(session.cookies) + '\n')
    log.write("SESSION RESTAPI KEY GET HEADER: " + str(rest_api_key.headers) + '\n')
    log.write("SESSION RESTAPI KEY GET TXT: " + str(rest_api_key.text) + '\n\n')

    time.sleep(0.2)

    timer_session = session.get(
        url=f"https://portail.cje.qc.ca/pluriportail/pfr/TimerSess.srf?Timer=OUI&_={round(time.time())}",
        headers=rest_api_key_header)

    log.write("SESSION TIMER STATUS: " + str(timer_session.status_code) + '\n')
    log.write("SESSION TIMER COOKIES: " + str(timer_session.cookies) + '\n')
    log.write("SESSION TIMER HEADER: " + str(timer_session.headers) + '\n')
    log.write("SESSION TIMER TXT: " + str(timer_session.text) + '\n\n')

    return session

# <----- AGENDA ----->
# PERMISSIONS = OPCODE 100
# CONTENTS = OPCODE 110
# TODO REV ENG AGENDA JS
def getAgenda(session, start, end):
    bcolors.Logging.info(thread="session/agenda", error="Getting agenda")
    unixStart = "1714363200000"
    unixEnd = "1715399999999"
    params = {
        "OP": "110",
        "noEcole": "-1",
        "mode": "2",
        "dateDebut": unixStart,
        "dateFin": unixEnd,
        "_": int(time.time())
    }

    agenda_header = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'X-PluriToken': csrf_token,
        'X-Requested-With': 'XMLHttpRequest',
        'Host': 'portail.cje.qc.ca',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://portail.cje.qc.ca/pluriportail/pfr/Main.srf?P=MainAccueil',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }

    agendadata = session.get(url=f"{agenda_url}?{urlencode(params)}", headers=agenda_header)

    return agendadata.text
