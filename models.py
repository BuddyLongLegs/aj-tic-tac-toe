from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

__all__=["PrivateBoards", "GroupBoards", "session"]

Base = declarative_base()
 
class PrivateBoards(Base):
    __tablename__ = 'privateboards'
    id = Column(Integer, primary_key = True)
    user_name = Column(String)
    board = Column(String)
    games = Column(Integer, default = 0)
    win=Column(Integer, default = 0)
    lose = Column(Integer, default = 0)
    tie = Column(Integer, default = 0)
        

class GroupBoards(Base):
    __tablename__ = "groupboards"
    id = Column(String, primary_key=True)
    player1 = Column(String)
    player2 = Column(String)
    board = Column(String)


engine = create_engine('sqlite:///data.db')

try:
    Base.metadata.create_all(engine)
except OperationalError:
    pass

session=Session(engine)

