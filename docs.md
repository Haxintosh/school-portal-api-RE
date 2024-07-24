# API docs
## Auth
### Login
```python
from api import *
login(username, password)
```
Login to the portal
#### Return
Returns a `Request.session` object that is authenticated to the portal servers, use it for other API requests that needs auth.  
It is recommended to save your credentials in a `.env` file, see main.py for an example. 
### Logout
```python
from api import *
logout(session)
```
Logout of the session
#### Return
Void
### Renew timer (NOT IMPLEMENTED)
```python
from api import *
renewTimer(session)
```
The session needs to be renewed if you are planning to use the same for requests over a long span of time, but you can just run the login for a new session and use that session instead of renewing
#### Return
Seconds to session expiration
## Agenda
### Get agenda
```python
from api import *
getAgenda(session, start, end)
```
session is an authenticated session object  
start is the epoch timestamp of **beginning** of the agenda to get  
end is the epoch timestamp of **end** of the agenda to get
#### Return
An array of day objects containing all the details of the day and the classes of the day in an array.
See below for examples (using `response.__repr__()`)
```json
[
   {
      "dayNum":"Jour 69",
      "date":1714363200.0,
      "type":0,
      "courses":[
         {
            "subject":"Math-SN",
            "day":1714363200.0,
            "start":1714397100.0,
            "end":1714401600.0,
            "teacher":"TEACHER NAME",
            "location":"B-312",
            "tasks":[
               {
                  "title":"TASK TITLE",
                  "type":1, 
                  "typeV2":0,
                  "isGraded":false,
                  "isDue":false,
                  "submittable":false
               }
            ],
            "id":"2023-501-MATSN406   -04   -1-00094"
         }
      ]
   },
   {
      "dayNum":"Jour 70",
      "date":1714449600.0,
      "type":0,
      "courses":[
         {
            "subject":"English",
            "day":1714449600.0,
            "start":1714478700.0,
            "end":1714483200.0,
            "teacher":"Ben Dover",
            "location":"B-291",
            "tasks":[
               
            ],
            "id":"SCHOOLYEAR-501-COURSEID     -GRP   -1-00094"
         }
      ]
   }
]
```
## Grades
### Get grades 
```python
from api import *
getGrades(session, semester)
```
semester is the semester of grades to fetch, 4 available options, 1 , 2, 3 or all
#### Return
Returns a list of exams in the chosen semester
```json
[
   {
      "date":"Mar 21 nov 2023",
      "type":"Comp. de texte",
      "name":"XYZ",
      "data":[
         "2023",
         "501",
         "ANGR409",
         "09",
         "1",
         "1",
         "20231121",
         "0",
         "20231121",
         "0"
      ],
      "competency":"C2",
      "weight":"0",
      "maxRes":"100",
      "res":"69.0",
      "resPercent":"(69.0%)"
   }
]
```
## Messages
### Overview
```python
from api import *
getMessages(session)
```
An overview of the inbox
#### Return
Array of messages without the contents (a rough overview of the messages)  
It provides an ID to use with `getMessageById(ID)` to get the specific message  
```json
[
   {
      "sender":"XYZ (role)",
      "title":"TITLE",
      "time":"2024/06/27 - 18:08",
      "receiver":"Élève - Gr. 920",
      "id":"1+1604494+2+0+0+0+1"
   },
   {
      "sender":"AUTHOR (ROLE)",
      "title":"TITLE",
      "time":"TIME",
      "receiver":"RECEIVER",
      "id":"ID"
   }
]
```
### Get message by ID
```python
from api import *
getMessageById(session, ID)
```
The ID is the message ID you can get via `getMessages()`
#### Returns
The files section provide links for downloading attached files, pass the link to the `downloadFile()` function along with the session
```json
{
   "message":"Bla bla message body here",
   "files":[
      {
         "name":"xyz.pdf",
         "link":"Telecharger.srf?TypeBlob=6&IdItem=SIEDNUENDUENDKENKJENFD57RH4U5GF45GFYD8UH3Fichier=1&Contexte=Courriel"
      }
   ],
   "subject":"SUBJECT",
   "from":"SENDER (ROLE)",
   "to":"RECEIVER (ROLE)",
   "date":"YYYY/MM/DD - HH:MM"
}
```
### Get all messages recursively
```python
from api import *
getAllMessageRecursive(session)
```
This function firsts get all message overviews and then get the contents of each message
#### Returns
An array of message overviews with a data field attached containing the content of the message (like the one you would get in `getMessageById()`)
```json
[
   {
      "sender":"AUTHOR (ROLE)",
      "title":"TITLE",
      "time":"TIME",
      "receiver":"RECEIVER",
      "id":"ID",
      "data":{
        "message":"Bla bla message body here",
         "files":[
           {
             "name":"xyz.pdf",
             "link":"Telecharger.srf?TypeBlob=6&IdItem=SIEDNUENDUENDKENKJENFD57RH4U5GF45GFYD8UH3Fichier=1&Contexte=Courriel"
           }
         ],
        "subject":"SUBJECT",
        "from":"SENDER (ROLE)",
        "to":"RECEIVER (ROLE)",
        "date":"YYYY/MM/DD - HH:MM"
      }
   }
]
```

