import sys
from .game_actions import *

class Game:
    #game variables
    difficulty = 6
    last_proof = 0
    next_proof = 0
    mining_room = 0
    snitch_room = 0
    well_room = 55
    dark_well_room = 555

    #tools
    def mine(self, last_proof):
        Game.last_proof = last_proof
        Game.next_proof = Mine(Game.last_proof, Game.difficulty)
        return Game.next_proof
    def decipher_clue(self, clue, current_room = 0):
        room = Decipher_Clue(clue)
        if current_room < 500: Game.mining_room = room
        else: Game.snitch_room = room
        return room

    #getters
    def get_last_proof(self): return Game.last_proof
    def get_next_proof(self): return Game.next_proof
    def get_mining_room(self): return Game.mining_room
    def get_snitch_room(self): return Game.snitch_room
    def get_well_room(self): return Game.well_room
    def get_dark_well_room(self): return Game.dark_well_room

    #setters
    def set_last_proof(self, proof): Game.last_proof = proof
    def set_difficulty(self, difficulty): Game.difficulty = difficulty