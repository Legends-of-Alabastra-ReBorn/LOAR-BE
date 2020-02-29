import time
from shortest_path import shortest_path

def traverse(player, destination):
    #find a path to the destination
    path = shortest_path(player.current_room, destination, player.abilities)
    print(f'{player.name} is traveling to room {destination}')
    print(f"{player.name}'s path: {path}")

    while path is not None:
        #must be faster to teleport to the beginning
        if path[0] is 'recall' and 'recall' in player.abilities:
            room_info = player.recall()
            print(f'{player.name} recalled to room {room_info["room_id"]}')

        elif 'dash' in player.abilities and len(path) > 1 and path[0][1] == path[1][1]:
            room_ids = []
            current_direction = path[0][1]
            for room in path:
                if room[1] == current_direction: room_ids.append(room[0])
                else: break
            room_info = player.dash_to(current_direction, room_ids)
            print(f'{player.name} dashed through {room_ids} to room {room_ids[-1]}')
        
        else:
            room_info = player.move_to(path[0][1], path[0][0])
            print(f'{player.name} moved {path[0][1]} to room {path[0][0]}')

        path = shortest_path(player.current_room, destination, player.abilities)
    
    print(f'{player.name} has arrived at room {destination}.')
