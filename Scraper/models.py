from sqlalchemy import Column, ForeignKey, Integer, String,Float  
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class PlayerDB(Base):
    __tablename__ = "PLAYER"
    puid = Column(Integer, primary_key=True)
    pname = Column(String(75), nullable=True)
    ploc = Column(String(250), nullable=True)
    pclass = Column(String(50), nullable=True)
    pmemsince = Column(String(50), nullable=True)
    prating = Column(Integer, nullable=True)
    pnumevents = Column(Integer, nullable=True)
    pearnings = Column(String(50), nullable=True)

class RoundDB(Base):
    __tablename__ = "ROUND"
    rtuid = Column(Integer, primary_key = True)
    rrndnum = Column(Integer, primary_key = True)
    rpuid = Column(Integer, primary_key = True)
    rname = Column(String(50), nullable=True)
    rtier = Column(String(50), nullable=True)
    rdate = Column(String(50), nullable=True)
    rscore = Column(Integer, nullable=False)
    rrating = Column(Integer, nullable=False)
    reval = Column(Integer, nullable=False)
    rincl = Column(Integer, nullable=False)
    #player = relationship(PlayerDB)

engine = create_engine('sqlite:///temp.db')
Base.metadata.create_all(engine)
