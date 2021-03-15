#!/usr/bin/python3
from parser import * 
from time import sleep
from random import uniform
def main():
    player = Player(69045)
    player.addPlayerFromURL()
    player.addRoundsFromURL()
    player.printPlayerDetails()
    player.addPlayerToDB()


if __name__ == "__main__":
    main()

