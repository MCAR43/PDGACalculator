#!/usr/bin/python3
from parser import * 
from time import sleep
def main():
    playernums = [77387, 113942, 121293, 113966, 126851, 63765]
    for num in playernums:
        player = Player(num)
        player.addPlayerFromURL()
        player.addRoundsFromURL()
        player.printPlayerDetails()
        player.addPlayerToDB()
        sleep(1)



if __name__ == "__main__":
    main()
