import json
import time
import requests
import pusher

from .shortest_path import shortest_path
from .utilities import Get_Request_Header, Load_Files, Save_File

pusher_client = pusher.Pusher(
  app_id='957271',
  key='486260c7fadf87293227',
  secret='d2ba08d29c8aa4df42ef',
  cluster='us2',
  ssl=True
)

def Move_To(player_token, direction, room_id=None):
    header = Get_Request_Header(player_token)
    endpoint = Load_Files(['endpoints'])['move']['endpoint']
    data = {'direction': direction, 'next_room_id': str(room_id)}
    response = requests.post(url = endpoint, headers = header, data = json.dumps(data)).json()
    time.sleep(response['cooldown'])
    return response

def Dash(player_token, direction, room_ids):
    header = Get_Request_Header(player_token)
    endpoint = Load_Files(['endpoints'])['dash']['endpoint']
    next_room_ids = ','.join(room_ids)
    data = json.dumps({'direction': direction, 'num_rooms': str(len(room_ids)), 'next_room_ids': next_room_ids})
    response = requests.post(url = endpoint, headers = header, data = data).json()
    time.sleep(response['cooldown'])
    return response

def Recall(player_token):
    header = Get_Request_Header(player_token)
    endpoint = Load_Files(['endpoints'])['recall']['endpoint']
    response = requests.post(url = endpoint, headers = header).json()
    time.sleep(response['cooldown'])
    return response

def Examine(player_token, item):
    header = Get_Request_Header(player_token)
    endpoint = Load_Files(['endpoints'])['examine']['endpoint']
    data = json.dumps({'name': item})
    response = requests.post(url = endpoint, headers = header, data = data).json()
    time.sleep(response['cooldown'])
    return response

def Take(player_token, item):
    header = Get_Request_Header(player_token)
    endpoint = Load_Files(['endpoints'])['take']['endpoint']
    data = json.dumps({'name': item})
    response = requests.post(url = endpoint, headers = header, data = data).json()
    time.sleep(response['cooldown'])
    return response

def Get_Last_Proof(player_token):
    header = Get_Request_Header(player_token)
    endpoint = Load_Files(['endpoints'])['last_proof']['endpoint']
    response = requests.get(url = endpoint, headers = header).json()
    time.sleep(response['cooldown'])
    return response

def Send_Proof(player_token, proof):
    header = Get_Request_Header(player_token)
    endpoint = Load_Files(['endpoints'])['mine']['endpoint']
    data = json.dumps({'proof': int(proof)})
    response = requests.post(url = endpoint, headers = header, data = data).json()
    time.sleep(response['cooldown'])
    return response

def Warp(player_token, abilities):
    if 'warp' not in abilities:
        print('this player cant warp, bruh')
        return None
    header = Get_Request_Header(player_token)
    endpoint = Load_Files(['endpoints'])['warp']['endpoint']
    response = requests.post(url = endpoint, headers = header).json()
    time.sleep(response['cooldown'])
    return response

def Get_Clue(player):
    well_room = 55 if player.current_room < 500 else 555
    if player.current_room != well_room:
        player.traverse(well_room)
    return player.examine('WELL')['description'].split('\n')[2:]

def Traverse(player, destination, take_items=False, use_abilities=True):
    abilities = player.abilities if use_abilities else []
    #find a path to the destination
    path = shortest_path(player.current_room, destination, abilities)
    # pusher_client.trigger('my-channel', 'my-event', {'player': f'{player.name}', 'message': f'{player.name} is traveling to room {destination}'})
    # pusher_client.trigger('my-channel', 'my-event', {'player': f'{player.name}', 'message': f"{player.name}'s path: {path}" })
    print(f'{player.name} is traveling to room {destination}')
    print(f"{player.name}'s path: {path}")

    room_info = None

    while path is not None:
        #must be faster to teleport to the beginning
        if path[0] is 'recall' and 'recall' in abilities:
            player.recall()
            pusher_client.trigger('my-channel', 'my-event', { 'player': f'{player.name}', 'room': '0', 'message':f'{player.name} recalled to room 0' })
            print(f'{player.name} recalled to room 0')

        elif 'dash' in abilities and len(path) > 1 and path[0][1] == path[1][1]:
            room_ids = []
            current_direction = path[0][1]
            for room in path:
                if room[1] == current_direction: room_ids.append(room[0])
                else: break
            room_info = player.dash_to(current_direction, room_ids)
            print(f'{player.name} dashed through {room_ids} to room {room_ids[-1]}')
            pusher_client.trigger('my-channel', 'my-event', {'player': f'{player.name}', 'room': f'{room_ids[-1]}', 'message': f'{player.name} dashed through {room_ids} to room {room_ids[-1]}' })
        
        else:
            room_info = player.move_to(path[0][1], path[0][0])
            print(f'{player.name} moved {path[0][1]} to room {path[0][0]}')
            pusher_client.trigger('my-channel', 'my-event', { 'player': f'{player.name}', 'room': f'{path[0][0]}', 'message': f'{player.name} moved {path[0][1]} to room {path[0][0]}' })
        
        if take_items:
            if 'items' in room_info:
                items = room_info['items']
                for item in items: print(player.take(item))

        path = shortest_path(player.current_room, destination, abilities)
    
    print(f'{player.name} has arrived at room {destination}.')
    pusher_client.trigger('my-channel', 'my-event', {'player': f'{player.name}', 'room': f'{destination}' })