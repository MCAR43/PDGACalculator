#!/usr/bin/python3
from parser import * 
from time import sleep
from random import uniform
def main():
    for num in range(69052, 69500):
        player = Player(num)
        print("Starting Scraping for Player: %s" % str(num))
        player.addPlayerFromURL()
        if not player.isexpired:
            print("Player has current PDGA")
            player.addRoundsFromURL()
            player.addPlayerToDB()
            player.printPlayerDetails()
        sleep(uniform(1,3))



if __name__ == "__main__":
    main()
