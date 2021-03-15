#!/usr/bin/python3
from parser import * 
from time import sleep
from random import uniform
def main():
    for i in range(100113, 100500):
        print("Checking for player: %d" % i)
        player = Player(i)
        player.addPlayerFromURL()
        #Make sure that rounds actually exist for this player
        if not player.p_expired:
            player.addRoundsFromURL()
            player.printPlayerDetails()
            player.addPlayerToDB()
            sleep(uniform(0.25, 0.5))


if __name__ == "__main__":
    main()

