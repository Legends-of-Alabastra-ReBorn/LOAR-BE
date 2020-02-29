import requests
import time

from utilities import Load_Files, Get_Request_Header

def Get_Player_Token(player_name):
    players = Load_Files(['players'])
    if player_name not in players:
        print(f'-------INVALID PLAYER NAME: {player_name}-------')
    else:
        return players[player_name]

def Get_Player_Info(player_name):
    header = Get_Request_Header(Get_Player_Token(player_name))
    endpoint = Load_Files(['endpoints'])['info']['endpoint']
    response = requests.get(url = endpoint, headers = header).json()
    time.sleep(response['cooldown'])
    return response

def Get_Player_Status(player_name):
    header = Get_Request_Header(Get_Player_Token(player_name))
    endpoint = Load_Files(['endpoints'])['status']['endpoint']
    response = requests.post(url = endpoint, headers = header).json()
    time.sleep(response['cooldown'])
    return response

def Get_Player_Abilities(player_name):
    return Get_Player_Status(player_name)['abilities']