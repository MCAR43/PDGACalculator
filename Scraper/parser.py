#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from collections import defaultdict 
from os import get_terminal_size
from dbctrl import insertPlayer
DETAILS_URI = "https://www.pdga.com/player/%s/details"
DEFAULT_URI = "https://www.pdga.com/player/%s"
class Player:
    def __init__(self, pid):
        self.pid = pid
        self.p_name = ""
        self.p_loc = ""
        self.p_class = ""
        self.p_memsince = ""
        self.p_rating = ""
        self.p_numevents = ""
        self.p_earnings = ""
        self.p_rounds = [] 

    def updatePlayer(self, details):
        if len(details) == 7:
            self.p_class, self.p_memsince, _, self.p_rating, self.p_numevents, _, self.p_earnings = details 
    
    def addRoundsFromURL(self):
        #page_response = requests.get(DETAILS_URI % self.pid).text
        with open('data/eric_data.html', 'r') as fp:
            soup = BeautifulSoup(fp, 'html.parser')
            playernumber = soup.find('meta', property="og:url").get('content')[::-1].split('/')[1]
            table = soup.find('table', id="player-results-details")
            for row in table.findAll('tr'):
                currounddetails = [playernumber]
                for elem in row.findAll('td'):
                    if elem.find('a') != None:
                        tuid = elem.find('a').get('href')[::-1].split('/')[0]
                        currounddetails.append(tuid)
                        currounddetails.append(elem.text)
                    else:
                        val = elem.text
                        currounddetails.append(val)
                    
                self.p_rounds.append(Round(currounddetails))

    def addPlayerFromURL(self):
        #page_response = requests.get(DEFAULT_URI % self.pid).text
        with open('data/eric.html', 'r') as fp:
            soup = BeautifulSoup(fp, 'html.parser')
            self.p_name = soup.find('meta', property="og:title").get('content').split('#')[0].strip()
            details = soup.find('ul', {'class': 'player-info'})
            self.p_loc = details.find('li', {'class': 'location'}).find('a').text
            pdet = []
            for li in details.findAll('li')[1:]:
                content = li.text.split(':')[1]
                if '(' in content:
                    content = content.split()[0]

                pdet.append(content.strip()) 

            self.updatePlayer(pdet[0:len(pdet) - 1])

    def printPlayerDetails(self):
        print("Player Name: %s" % self.p_name)
        print("Player Number: %s" % self.pid)
        print("Player Location: %s" % self.p_loc)
        print("Player Classification: %s" % self.p_class)
        print("Player Member Since: %s" % self.p_memsince)
        print("Player Rating: %s" % self.p_rating)
        print("Player Events Played: %s" % self.p_numevents)
        print("Player Earnings: %s" % self.p_earnings)
        print("Player Rounds: %s" % self.p_rounds)
        

    def addPlayerToDB(self):
        insertPlayer(self.pid, self.p_name, self.p_loc, self.p_class, self.p_memsince, self.p_rating, self.p_numevents, self.p_earnings)

                        

class Round:
    def __init__(self):
        self.puid = 0
        self.ruid = 0
        self.rname = ""
        self.tier = ""
        self.date = ""
        self.round = 0
        self.score = 0
        self.rrating = 0
        self.eval = 0
        self.incl = 0

    def __init__(self, details):
        #we know the order so we can jsut do this
        if len(details) == 10:
            self.puid, self.ruid, self.rname, self.tier, self.date, self.round, self.score, self.rrating, self.eval, self.incl = details
            self.printRound()
    
    def printRound(self):
        #TODO: Print Prettier Later
        numCol = get_terminal_size().columns
        print(numCol)
        print("# Player Number: %s" % self.puid)
        print("# Round Identifier: %s" % self.ruid)
        print("# Round Name: %s" % self.rname)
        print("# Round Tier: %s" % self.tier)
        print("# Round Date: %s" % self.date)
        print("# Round Num: %s" % self.round)
        print("# Round Score: %s" % self.score)
        print("# Round Rating: %s" % self.rrating)
        print("# Round Evaluated: %s" % self.eval)
        print("# Round Included: %s" % self.incl)
        print("#" * numCol)
  


'''
#ook ook bs4 can't into for eaches on tds
curRoundDetails = [] 
for row in table.findAll('tr'):
    for elem in row.find('td'):
        if elem.find('a') != None:
            #ooga booga don't want to import regex
            tuid = elem.find('a').get('href')[::-1].split('/')[0]
            print("tuid: %s" % tuid)
            curRoundDetails.append(tuid)
        else:
            val = elem.text
            curRoundDetails.append(val)
            print("%s: %s" % (elem.get('class')[0], elem.text))

    print(curRoundDetails)

'''


'''
    def addroundsfromfile(self, filepath):
        with open(filepath, 'r') as fp:
            soup = beautifulsoup(fp, 'html.parser')
            playernumber = soup.find('meta', property="og:url").get('content')[::-1].split('/')[1]
            table = soup.find('table', id="player-results-details")
            print(table)
            for row in table.findall('tr'):
                currounddetails = [playernumber]
                for elem in row.findall('td'):
                    if elem.find('a') != none:
                        tuid = elem.find('a').get('href')[::-1].split('/')[0]
                        currounddetails.append(tuid)
                    else:
                        val = elem.text
                        currounddetails.append(val)
                    
                round(currounddetails)
'''


















