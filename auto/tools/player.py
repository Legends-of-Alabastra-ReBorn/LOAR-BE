from game import Game
from player_info import *
from player_actions import *

class Player(Game):
    def __init__(self, name):
        self.name = name
        self.auth = Get_Player_Token(name)
        self.current_room = Get_Player_Info(name)['room_id']
        self.inventory = []
        self.coins = Get_Coin_Balance(self.auth)
        self.abilities = Get_Player_Abilities(name)

    #move player
    def get_status(self):
        return Get_Player_Status(self.name)
    def move_to(self, direction, destination):
        room_info = Move_To(self.auth, direction, destination)
        self.current_room = room_info['room_id']
        return room_info
    def dash_to(self, direction, room_ids):
        room_info = Dash(self.auth, direction, room_ids)
        self.current_room = room_info['room_id']
        return room_info
    def recall(self):
        room_info = Recall(self.auth)
        self.current_room = room_info['room_id']
        return room_info
    def warp(self):
        room_info = Warp(self.auth, self.abilities)
        self.current_room = room_info['room_id']
        return room_info
    def traverse(self, destination, take_items=False, use_abilities=True):
        Traverse(self, destination, take_items, use_abilities)
    def take(self, item):
        return Take(self.auth, item)['messages']

    #game changers
    def examine(self, item='WELL'):
        self.decipher_clue(Examine(self.auth, item)['description'], self.current_room)
    def last_proof(self):
        last_proof = Get_Last_Proof(self.auth)
        self.set_last_proof(last_proof['proof'])
        self.set_difficulty(last_proof['difficulty'])
    def send_proof(self, proof=None):
        if proof is None: proof = self.next_proof
        res = Send_Proof(self.auth, proof)
        if 'messages' in res and res['messages'][0] == 'New Block Forged':
            self.coins += 1
        return res