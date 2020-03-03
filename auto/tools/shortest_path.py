import sys
from pathlib import Path
import json

from .utilities import Queue, Load_Files

maps = Load_Files(['overworld','underworld'])
endpoints = Load_Files(['endpoints'])

#determine cooldown of entire path
def get_cooldown(path, world, abilities, DEBUG=False):
    cooldown = 0
    previous_room = ()
    for i in range(len(path)):
        room = path[i]
        room_id = room[0]
        current_direction = room[1]
        cooldown += get_room_cooldown(room_id, world) if i>0 else 0 #skip first room

        #DEBUG print room cooldowns
        if DEBUG: print(room_id, get_room_cooldown(room_id, world))

        #add dash functionality
        if 'dash' in abilities and i>1: #start checking at 3rd room
            previous_direction = previous_room[1]
            previous_cooldown = get_room_cooldown(previous_room[0], world)
            if previous_direction == current_direction:
                cooldown -= previous_cooldown
        previous_room = room
    return cooldown

def get_room_cooldown(room, world):
    if 'cooldown' in maps[world][room]: return maps[world][room]['cooldown']
    return 30

def shortest_path(start, end, abilities=()):
    if int(start) == int(end): return None
    if int(start) > 999 or int(start) < 0 or int(end) > 999 or int(end) < 0:
        print("room out of bounds, try again")
        return None
    if 'warp' not in abilities and (int(start) < 499 and int(end) > 499 or int(start) > 499 and int(end) < 499):
        print('you need the warp ability for that, bruh')
        return None
    world = 'overworld' if start < 500 else 'underworld'

    #initialize
    queue = Queue()
    start = str(start)
    end = str(end)
    path = {'path': [], 'weight': None}
    queue.enqueue({'room': start, 'path': [], 'weight': 0})
    if start != '0' and 'recall' in abilities:
        queue.enqueue({'room': '0', 'path': ['recall'], 'weight': 15})
    visited = {}

    while queue.size() > 0:
        current_room = queue.dequeue()
        exits = maps[world][current_room['room']]['exits']
        weight = current_room['weight']

        #there isn't going to be a shorter path than the one already found, skip it
        if path['weight'] is not None and weight >= path['weight']: continue

        #check to see if the exit is connect to current room
        #if so update path and check if it's shorter than current known path
        if end in exits and (path['weight'] is None or weight < path['weight']):
            path['path'] = current_room['path'] + [(end, exits[end])]
            path['weight'] = get_cooldown(path['path'], world, abilities)
            continue

        #add neighbors to queue
        for exit in exits:
            current_path = current_room['path'] + [(exit, exits[exit])]
            current_weight = get_cooldown(current_path, world, abilities)
            next_room = {'room': exit, 'path': current_path, 'weight': current_weight}
            if exit not in visited or current_weight < visited[exit]['weight']:
                visited[exit] = next_room
                queue.enqueue(next_room)

    return path['path']