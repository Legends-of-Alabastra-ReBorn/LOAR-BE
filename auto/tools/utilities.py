from pathlib import Path
import json

data_folder = Path('./data/')

def Get_Request_Header(player_token):
    return {'Content-Type': 'application/json', 'Authorization': player_token}

def Load_Files(files):
    data = {}
    for f in files:
        with open(f'{data_folder}/{f}.txt') as file_data:
            data[f] = json.load(file_data)
    if len(files) == 1:
        data = data[files[0]]
    return data

def Save_File(file, data):
    with open(f'{data_folder}/{file}.txt', 'w') as file_data:
        json.dump(data, file_data)

def Get_Room_ID(room):
    return Load_Files(['rooms'])[room]

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)