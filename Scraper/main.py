#!/usr/bin/python3
from parser import * 
from time import sleep
from random import uniform
def main():
    for i in range(100000, 100500):
        print("Checking for player: %d" % i)
        player = Player(i)
        player.addPlayerFromURL()
        if not player.p_expired:
            player.addRoundsFromURL()
            player.printPlayerDetails()
            player.addPlayerToDB()

        sleep(uniform(0.5, 1.5))

if __name__ == "__main__":
    main()

