#!/usr/bin/python3
from parser import * 
def main():
    player = Player(77387)
    player.addPlayerFromURL()
    player.addRoundsFromURL()
    player.printPlayerDetails()
    player.addPlayerToDB()


if __name__ == "__main__":
    main()
