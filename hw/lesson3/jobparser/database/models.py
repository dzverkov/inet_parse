from sqlalchemy import Table, Column, String, Integer

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    url = Column(String, nullable=True)
    spider = Column(String, nullable=True)
    name = Column(String, nullable=True)
    salary = Column(String, nullable=True)
    employer = Column(String, nullable=True)


    def __init__(self, **kwargs):
        self.url = kwargs.get('url')
        self.name = kwargs.get('name')
        self.spider = kwargs.get('spider')
        self.salary = kwargs.get('salary')
        self.employer = kwargs.get('employer')
        pass