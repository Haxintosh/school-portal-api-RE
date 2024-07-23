from api import *
from utils import *
from dotenv import load_dotenv
import os

load_dotenv('.env')

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

main_session = login(USERNAME, PASSWORD)

parseGrades(getGrades(main_session, 1))

# parseAgenda(getAgenda(main_session, start=0, end=0))