#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from collections import defaultdict 
from os import get_terminal_size
from dbctrl import insertPlayer, insertRound
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
        self.p_numwins = ""
        self.p_numevents = ""
        self.p_earnings = ""
        self.p_rounds = [] 
        self.p_expired = False
    
    # -------------------------------------------------------------------------------------------------------
    # PRE: 
    #   * This function should only ever be called AFTER Player#addPlayerFromURL has been called
    #   * Will return if certain fields are not defined previously (indicating that the above was not filled)
    #
    # DEF:
    #   * Will fill later
    # -------------------------------------------------------------------------------------------------------
    def addRoundsFromURL(self):
        fp = requests.get(DETAILS_URI % self.pid).text
        soup = BeautifulSoup(fp ,'html.parser')
        table = soup.find('table', id='player-results-details')
        #Weird PDGA glitch where they have > 0 events but their is nothing on their round ratings page, this takes care of that 
        if table is None:
            return

        print("passed weird glitch")
    
        for entry in table.findAll('tr')[1:]:
            #Every tournament ID entry follows the following format
            # "/tour/event/39523"
            # to avoid importing re just split by the / and grab the end
            tournamentID = entry.find('td', {'class': 'tournament'}).find('a').get('href').split('/')[-1]
            tournamentName = entry.find('a').text
            tournamentTier = entry.find('td', {'class': 'tier'}).text

            #PDGA is not at all consistent with their formatting for tournament dates, we are only concerned with the end date of the tournament for rating calculations
            # Our rating calculator will be off by 1-2 days, but I don't think the PDGA even accounts for this
            # TODO: We need to translate these stupid dates that say 07 aug - 09 aug into N separate dates corresponding to the round numbers so we can get day to day calcs for ratings
            # TODO: Email the PDGA and tell them how much I despise them
            tournamentDate = entry.find('td', {'class': 'date'}).text
            if ' ' in tournamentDate:
                tournamentDate = tournamentDate.split(' ')[-1]

            tournamentRoundNum = entry.find('td', {'class': 'round'}).text
            tournamentScore = entry.find('td', {'class': 'score'}).text
            tournamentRoundRating = entry.find('td', {'class': 'round-rating'}).text
            tournamentEval = entry.find('td', {'class': 'evaluated'}).text
            tournamentIncl = entry.find('td', {'class': 'included'}).text
            self.p_rounds.append(Round(self.pid, tournamentID, tournamentName, tournamentTier, tournamentDate, tournamentRoundNum, tournamentScore, tournamentRoundRating, tournamentEval, tournamentIncl))

    # -------------------------------------------------------------------------------------------------------
    # PRE: 
    #   * do later
    # DEF:
    #   * Will fill later
    # -------------------------------------------------------------------------------------------------------

    def addPlayerFromURL(self):
        fp = requests.get(DEFAULT_URI % self.pid).text
        soup = BeautifulSoup(fp ,'html.parser')
        #Checks for the player being expired or the page not being found and skips parsing
        if self.isPlayerExpired(soup):
            self.p_expired = True
            return

        details = soup.find('ul', {'class': 'player-info'})
        self.p_loc = details.find('li', {'class':'location'}).find('a').text
        self.p_name = soup.find('meta', property="og:title").get('content').split('#')[0].strip()
        #Most of these fields follows this format for parsing
        # "JunkText: VALUENEEDED potentiallmorejunkafter
        # Parsing for VALUENEEDED is done by splitting the text by ':' and selecting the second element in the list then stripping whitespace 
        self.p_class = details.find('li', {'class':'classification'}).text.split(':')[1].strip()
        self.p_memsince = details.find('li', {'class', 'join-date'}).text.split(':')[1].strip()

        #The above will be on EVERY single PDGA profile, these may or may not exist.
        #TODO:This is pretty dumb, should fix later
        try:
            self.p_numwins = details.find('li', {'class', 'career-wins'}).text.split(':')[1].strip()
        except AttributeError:
            self.p_numwins = 0
        try:
            self.p_rating = details.find('li', {'class', 'current-rating'}).text.split(':')[1].split()[0]
        except AttributeError:
            self.p_rating = 0
        try:
            self.p_numevents = details.find('li', {'class', 'career-events'}).text.split(':')[1].strip()
        except AttributeError:
            self.p_numevents = 0
        try:
            self.p_earnings = details.find('li', {'class', 'career-earnings'}).text.split(':')[1].strip()
        except AttributeError:
            self.p_earnings = 0

    # -------------------------------------------------------------------------------------------------------
    # PRE: 
    #   * do later
    # DEF:
    #   * Will fill later
    # -------------------------------------------------------------------------------------------------------

    def isPlayerExpired(self, soup):
        expirySearch = soup.findAll(text='Expired')
        pageNotFoundErrorSearch = soup.findAll(text='Page not found')
        if expirySearch != [] or pageNotFoundErrorSearch != []:
            self.isexpired = True
            return True
        else:
            self.isexpired = False 
            return False

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
        if self.p_rounds:
            for rnd in self.p_rounds:
                rnd.addRoundToDB()

    
                        

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

    def __init__(self, pid, tuid, name, tier, date, roundnum, score, rrating, evl, incl):
        self.puid = pid
        self.ruid = tuid
        self.rname = name
        self.tier = tier
        self.date = date
        self.round = roundnum
        self.score = score
        self.rrating = rrating
        self.eval = evl
        self.incl = incl
    
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

    def addRoundToDB(self):
        insertRound(self.ruid, self.round, self.puid, self.rname, self.tier, self.date, self.score, self.rrating, self.eval, self.incl)
