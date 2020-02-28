import requests
import random
import json
import time
from shortest import shortest_path
counter = 0
get_headers = {
  "Authorization": "Token 837aeca1c04015da897b2fc93d98cad28e917e02"
}
move_headers = {
  "Authorization": "Token 837aeca1c04015da897b2fc93d98cad28e917e02",
  "content-type": "application/json"
}
info_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/"
r = requests.get(url = info_url, headers = get_headers)
data = r.json()
print(data)
cooldown = data['cooldown']
time.sleep(cooldown)
current_room = data['room_id']
path = shortest_path(current_room, 5, 'overworld', ())
while counter < len(path):
  direction = path[counter][1]
  if not direction:
    counter += 1
    break
  move_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"
  move_data = {"direction": direction}
  move = requests.post(url = move_url, data = json.dumps(move_data), headers = move_headers)
  data = move.json()
  cooldown = data['cooldown']
  time.sleep(cooldown)
  def get_info():
    r = requests.get(url = info_url, headers = get_headers)
    data = r.json()
    print(data)
    return data
  info = get_info()
#   items = info['items']
  cooldown = info['cooldown']
  time.sleep(cooldown)
#   if items is not None:
#     x = 0
#     while x < len(items):
#       y = requests.post(url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/take/", data = json.dumps({"name":"tiny treasure"}), headers = move_headers)
#       d = y.json()
#       time.sleep(d['cooldown'])
#       x += 1
  counter += 1
print('reached our destination!')