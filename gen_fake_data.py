import sqlite3
import random
from mimesis import Generic
import datetime
from datetime import date
from typing import List, Tuple

SURVEYS_COUNT = 5
MAX_QUESTIONS_PER_SURVEY_COUNT = 7
MAX_CHOICES_PER_QUESTION_COUNT = 4

conn = sqlite3.connect('sqlite3.db')
conn.row_factory = sqlite3.Row
# cursor = conn.cursor()

fake_gen = Generic('ru')


def fill_surveys():
    q = "INSERT INTO 'surveys' (title, start_date, end_date, description, created_at, updated_at)\n"
    for i in range(SURVEYS_COUNT):
        title = f"Survey about {fake_gen.text.words(quantity=1)[0]}"
        start_date = fake_gen.datetime.datetime(start=2018, end=2021)
        end_date = start_date + datetime.timedelta(days=15)
        start_date_str = start_date.strftime("%B %d, %Y %I:%M%p")
        end_date_str = end_date.strftime("%B %d, %Y %I:%M%p")
        description = fake_gen.text.text(quantity=3)
        # TODO: написание запроса можно так не дублировать
        if i == 0:
            q += (f"SELECT '{title}' AS 'title', "
                  f"'{start_date_str}' AS 'start_date', "
                  f"'{end_date_str}' AS 'end_date', "
                  f"'{description}' AS 'description', "
                  f"'{start_date_str}' AS 'created_at', "
                  f"'{start_date_str}' AS 'updated_at'\n"
                  )
            continue
        q += (f"UNION SELECT '{title}' AS 'title', "
              f"'{start_date_str}' AS 'start_date', "
              f"'{end_date_str}' AS 'end_date', "
              f"'{description}' AS 'description', "
              f"'{start_date_str}' AS 'created_at', "
              f"'{start_date_str}' AS 'updated_at'\n"
              )
    cursor = conn.execute(q)
    conn.commit()
    cursor.close()


def get_surveys():
    q = "SELECT * FROM 'surveys'"
    cursor = conn.execute(q)
    while True:
        row = cursor.fetchone()
        if not row:
            break
        yield row
    cursor.close()


# TODO выделить в отдельный метод получение всех строк
def get_questions():
    q = "SELECT * FROM 'questions'"
    cursor = conn.execute(q)
    while True:
        row = cursor.fetchone()
        if not row:
            break
        yield row
    cursor.close()


def random_question_type():
    type_num = random.randint(0, 2)
    return ['single_choice', 'multiple_choice', 'text'][type_num]


def fill_questions():
    q = "INSERT INTO 'questions' (survey_id, title, number, type, created_at, updated_at)\n"
    # сделать генератор, который будет возвращать словарь с инфой о строке
    first_row = True
    for survey in get_surveys():
        questions_count = random.randint(1, MAX_QUESTIONS_PER_SURVEY_COUNT)
        for j in range(questions_count):
            survey_id = survey['id']
            title = fake_gen.text.text(quantity=1)
            number = j + 1
            type_ = random_question_type()
            updated_at_str = created_at_str = datetime.datetime.now().strftime("%B %d, %Y %I:%M%p")
            if first_row:
                q += (f"SELECT {survey_id} AS 'survey_id', "
                      f"'{title}' AS 'title', "
                      f"{number} AS 'number', "
                      f"'{type_}' AS 'type', "
                      f"'{created_at_str}' AS 'created_at', "
                      f"'{updated_at_str}' AS 'updated_at'\n"
                      )
                first_row = False
                continue
            q += (f"UNION SELECT {survey_id} AS 'survey_id', "
                  f"'{title}' AS 'title', "
                  f"{number} AS 'number', "
                  f"'{type_}' AS 'type', "
                  f"'{created_at_str}' AS 'created_at', "
                  f"'{updated_at_str}' AS 'updated_at'\n"
                  )
    cursor = conn.execute(q)
    conn.commit()
    cursor.close()


def fill_choices():
    q = "INSERT INTO 'choices' (question_id, number, text, created_at, updated_at)\n"
    first_row = True
    for question in get_questions():
        if question['type'] == 'text':
            continue
        choices_count = random.randint(1, MAX_CHOICES_PER_QUESTION_COUNT)
        for j in range(choices_count):
            question_id = question['id']
            number = j + 1
            text = fake_gen.text.text(quantity=1)
            updated_at_str = created_at_str = datetime.datetime.now().strftime("%B %d, %Y %I:%M%p")
            if first_row:
                q += (f"SELECT {question_id} AS 'question_id', "
                      f"{number} AS 'number', "
                      f"'{text}' AS 'text', "
                      f"'{created_at_str}' AS 'created_at', "
                      f"'{updated_at_str}' AS 'updated_at'\n"
                      )
                first_row = False
                continue
            q += (f"UNION SELECT {question_id} AS 'question_id', "
                  f"{number} AS 'number', "
                  f"'{text}' AS 'text', "
                  f"'{created_at_str}' AS 'created_at', "
                  f"'{updated_at_str}' AS 'updated_at'\n"
                  )
    cursor = conn.execute(q)
    conn.commit()
    cursor.close()


fill_surveys()
fill_questions()
fill_choices()
