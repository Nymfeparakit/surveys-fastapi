import sqlite3


SURVEYS_COUNT = 5
MAX_QUESTIONS_PER_SURVEY_COUNT = 7
MAX_CHOICES_PER_QUESTION_COUNT = 4

conn = sqlite3.connect('sqlite3.db')
cursor = conn.cursor()

def fill_surveys():
    q = "INSERT INTO 'surveys'"
    for i in range(SURVEYS_COUNT):
       title = None
       start_date = None
       end_date = None 
       description = None
       if i == 0:
           q += f"SELECT '{title}' AS 'title', {start_date} AS 'start_date', {end_date} AS 'end_date', '{description}' AS 'description'"
           break
    cursor.execute(q)
    cursor.close()


def fill_questions():
    pass

def fill_choices():
    pass