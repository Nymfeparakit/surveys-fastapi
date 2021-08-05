from re import L
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    TIMESTAMP,
    String,
    Date,
    Text,
    ForeignKey,
    SmallInteger,
    Enum
)
from sqlalchemy.orm import relationship
import datetime
import enum


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now())


class Survey(BaseModel):
    """
    Модель опроса
    """
    __tablename__ = 'surveys'

    title = Column(String(64), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    description = Column(Text)
    questions = relationship('Question', backref='survey', order_by='Question.number')


class QuestionType(enum.Enum):
    single_choice = 1
    multiple_choice = 2
    text = 3


class Question(BaseModel):
    """
    Вопрос, содержащийся в опросе
    """
    __tablename__ = 'questions'

    survey_id = Column(Integer, ForeignKey('surveys.id'))
    title = Column(String(64), nullable=False)
    number = Column(SmallInteger, nullable=False) # порядковый номер в опросе
    type = Column(Enum(QuestionType), nullable=False)
    choices = relationship('QuestionChoice', backref='question', order_by='QuestionChoice.number')


class QuestionChoice(BaseModel):
    """
    Вариант ответа на вопрос
    """
    __tablename__ = 'choices'

    question_id = Column(Integer, ForeignKey('questions.id'))
    text = Column(String(64), nullable=False)
    number = Column(Integer, nullable=False)
