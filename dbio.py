# dbio.py // @toblobs

from __init__ import *
from question import Question, Response
from led import *

dbc = sqlite3.connect(DATABASE_FILE)
cursor = dbc.cursor()

#cursor.execute("""CREATE TABLE questions(
#               question_id INTEGER PRIMARY KEY, 
#               question TEXT, 
#               leds TEXT
#               );""")

#cursor.execute("""CREATE TABLE responses(
#               response_id INTEGER PRIMARY KEY,
#               question_id INTEGER,
#               response INTEGER,
#               user_id TEXT,
#               datetime TEXT,
#               FOREIGN KEY (question_id) REFERENCES questions (question_id)
#               );""")

def save_question(q: Question):

    data = [q.id, q.question, '\n'.join(str(l) for l in q.leds)]
    cursor.execute(f"INSERT INTO questions VALUES(?, ?, ?)", data)

    dbc.commit()

def fetch_question(id):

    tup = cursor.execute(f"SELECT * FROM questions WHERE question_id = {id}").fetchone()

    return Question(tup[0], tup[1], [create_display_from_emojis(t) for t in tup[2].split('\n\n')])

def save_response(r: Response):

    data = [r.id, r.question_id, r.response, r.user_id, int(r.datetime.timestamp())] 
    cursor.execute(f"INSERT INTO responses VALUES(?, ?, ?, ?, ?)", data)

    dbc.commit()

def fetch_response(id):

    tup = cursor.execute(f"SELECT * FROM responses WHERE response_id = {id}").fetchone()

    return Response(tup[0], tup[1], tup[2], tup[3], datetime.fromtimestamp(int(tup[4])))

def get_questions_length():

    return cursor.execute('SELECT COUNT(*) FROM questions').fetchone()[0]

def get_responses_length():

    return cursor.execute('SELECT COUNT(*) FROM responses').fetchone()[0]