from api import *
from utils import *
from dotenv import load_dotenv
import os

load_dotenv('.env')

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

main_session = login(USERNAME, PASSWORD)

# print(getAgenda(session=main_session, start=1714363200000, end=1715399999999).__repr__())
# getMessages(main_session)
getMessageById(main_session, '1+1604494+2+0+0+0+1')
# print(getGrades(main_session, 2))
# getAllMessageRecursive(main_session)
# downloadFile(main_session, "Telecharger.srf?TypeBlob=6&IdItem=F47A7B1DB3BF739B53155A60C22D683838FFF5E16E7E095090803E65DDF14E78&IdFichier=1&Contexte=Courriel")