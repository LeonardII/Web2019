import random
from dataModels import *
from run import db

def jsonInsert(data):
    e = []
    for q in data:
        new_entry = Question(
         Frage=q['Frage'],
         Option_eins=q['Optionen'][0],
         Option_zwei=q['Optionen'][1],
         Option_drei=q['Optionen'][2],
         Option_vier=q['Optionen'][3],
          Antwort=q['Antwort'])
        e.append(new_entry)
        i+=1
    
    db.session.add_all(e)
    db.session.commit()

def insertQuestion(frage, optionen, antwort):
    if(len(optionen)==4):
        q = Question(Frage=frage,Option_eins=optionen[0],Option_zwei=optionen[1],Option_drei=optionen[2],Option_vier=optionen[3],Antwort=antwort)
        db.session.add(q)
        db.session.commit()

def getRandomQuestion():
    rand = random.randrange(0, session.query(Question).count())
    row = session.query(Question)[rand]
    return row
        

def addUser(name, email, passwort):
    u = User(Name=name, Email=email, Passwort=passwort)
    db.session.add(u)
    db.session.commit()

def loginUser(email, passwort):
    q = session.query(User).filter(User.Email == email, User.Passwort == passwort)
    exists = session.query(q.exists())
    db.session.commit()
    return exists

