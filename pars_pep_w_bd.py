from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, declared_attr, declarative_base
import requests
from bs4 import BeautifulSoup
import re


PEP_URL = 'https://peps.python.org/'

Base = declarative_base()


class Pep(Base):
    __tablename__ = 'Pep'
    id = Column(Integer, primary_key=True)
    type_status = Column(String(2))
    number = Column(Integer, unique=True)
    title = Column(String(200))
    authors = Column(String(20))

    def __repr__(self):
        return f'PEP {self.pep_number} {self.name}'

engine = create_engine('sqlite:///sqlite.db')
session_bd = Session(engine)

if __name__ == '__main__':
    response = requests.get(PEP_URL)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, features='lxml')
    Base.metadata.create_all(engine) 
    main_tag = soup.find( 
        'section', 
        {'id': 'numerical-index'} 
    ) 
    pep_row = main_tag.find_all('tr')
    for pip in range(1, len(pep_row)):
        tr = pep_row[pip]
        version_a_tag = tr.find('a')
        status = tr.find('abbr').text
        number = version_a_tag.text
        title = tr.find_all('td')[2].text
        author = tr.find_all('td')[3].text
        session_bd.add(
            Pep(
                type_status=str(status),
                number=int(number),
                title=str(title),
                authors=str(author)
            )
        )
        
session_bd.commit()
