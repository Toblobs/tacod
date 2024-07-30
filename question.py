# question.py // @toblobs

from __init__ import *

class Question:

    def __init__(self, id: int, question: str, leds: iter):

        self.id = id
        self.question = question
        self.leds = leds

class Response:

    def __init__(self, id: int, question_id: int, response: int, user_id: str, datetime: datetime):

        self.id = id
        self.question_id = question_id

        self.response = response

        self.user_id = user_id
        self.datetime = datetime

# question generation goes here...

