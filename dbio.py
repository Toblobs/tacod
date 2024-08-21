# dbio.py // @toblobs

from __init__ import *
from question import Question, Response
from led import *

global db_lock
db_lock = asyncio.Lock()

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

async def save_question(q: Question):

    async with db_lock:

        data = [q.id, q.question, '\n'.join(str(l) for l in q.leds)]
        cursor.execute(f"INSERT INTO questions VALUES(?, ?, ?)", data)

        dbc.commit()

async def fetch_question(id):

    async with db_lock:

        tup = cursor.execute(f"SELECT * FROM questions WHERE question_id = {id}").fetchone()

        return Question(tup[0], tup[1], [create_display_from_emojis(t) for t in tup[2].split('\n\n')])

async def save_response(r: Response):

    async with db_lock:

        data = [r.id, r.question_id, r.response, r.user_id, int(r.datetime.timestamp())] 
        cursor.execute(f"INSERT INTO responses VALUES(?, ?, ?, ?, ?)", data)

        dbc.commit()

async def fetch_response(id):

    async with db_lock:

        tup = cursor.execute(f"SELECT * FROM responses WHERE response_id = {id}").fetchone()

        return Response(tup[0], tup[1], tup[2], tup[3], datetime.fromtimestamp(int(tup[4])))

async def get_questions_length():

    async with db_lock:

        return cursor.execute('SELECT COUNT(*) FROM questions').fetchone()[0]

async def get_responses_length():

    async with db_lock:

        return cursor.execute('SELECT COUNT(*) FROM responses').fetchone()[0]
    

async def get_confidence_threshold():

    global CONDFIDENCE_THRESHOLD
    CONFIDENCE_THRESHOLD =  0.1 # pow(e, await get_responses_length() / 4500) - 1

    return CONFIDENCE_THRESHOLD