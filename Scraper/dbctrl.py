#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, PlayerDB, RoundDB
engine = create_engine('sqlite:///temp.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

def insertPlayer(puid, pname, ploc="", pclass="", pmemsince="", prating=0, pnumevents=0, pearnings=0):
    tempPlayerObject = PlayerDB(puid=puid, pname=pname, ploc=ploc, pmemsince=pmemsince, prating=prating, pnumevents=pnumevents, pearnings=pearnings)
    session.add(tempPlayerObject)
    session.commit()

