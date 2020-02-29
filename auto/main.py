import sys
import asyncio
import random

sys.path.insert(1, './tools')
from player import Player

def main():
    print('-------SETTING UP-------')
    players = [Player('doug'),Player('mike'),Player('miguel')]
    current_player = 0
    proof = 0
    while True:
        current_player = random.randint(0,len(players)-1)
        if current_player == len(players): current_player = 0
        players[current_player].traverse(players[current_player].get_well_room())
        players[current_player].examine()
        players[current_player].last_proof()
        print('mining room: ', players[current_player].get_mining_room())
        print('last proof:', players[current_player].get_last_proof())
        if proof != players[current_player].get_last_proof():
            proof = players[current_player].get_last_proof()
            players[current_player].mine()
        players[current_player].traverse(players[current_player].get_mining_room())
        print('sending proof:', players[current_player].get_next_proof())
        players[current_player].send_proof()

main()