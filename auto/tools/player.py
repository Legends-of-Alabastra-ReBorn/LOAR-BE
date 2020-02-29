from game import Game
from player_info import *
from player_actions import *

class Player(Game):
    def __init__(self, name):
        self.name = name
        self.auth = Get_Player_Token(name)
        self.current_room = Get_Player_Info(name)['room_id']
        self.inventory = []
        self.abilities = Get_Player_Abilities(name)

    #move player
    def move_to(self, direction, destination):
        self.current_room = Move_To(self.auth, direction, destination)['room_id']
    def dash_to(self, direction, room_ids):
        self.current_room = Dash(self.auth, direction, room_ids)['room_id']
    def recall(self):
        self.current_room = Recall(self.auth)['room_id']
    def warp(self):
        self.current_room = Warp(self.auth, self.abilities)['room_id']
    def traverse(self, destination):
        Traverse(self, destination)

    #game changers
    def examine(self, item='WELL'):
        self.decipher_clue(Examine(self.auth, item)['description'], self.current_room)
    def last_proof(self):
        last_proof = Get_Last_Proof(self.auth)
        self.set_last_proof(last_proof['proof'])
        self.set_difficulty(last_proof['difficulty'])
    def send_proof(self):
        _ = Send_Proof(self.auth, self.next_proof)