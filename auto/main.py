import multiprocessing as mp
import time
import pusher
from shutdown import *
# sys.path.insert(1, './tools')
from .tools.player import Player
from .tools.game import Game
from .mulligan import toggle

pusher_client = pusher.Pusher(
  app_id='957271',
  key='486260c7fadf87293227',
  secret='d2ba08d29c8aa4df42ef',
  cluster='us2',
  ssl=True
)

def miner(last_proof, next_proof, miner_name):
    print(f'initializing miner {miner_name}')
    miner = Game()
    current_proof = 0
    while True:
        time.sleep(1)
        if current_proof != last_proof.value:
            current_proof = last_proof.value
            print(f'{miner_name} is mining with proof {current_proof}...')
            miner.mine(current_proof)
            print(f'{miner_name} found proof {miner.get_next_proof()}')
            next_proof.value = miner.get_next_proof()

def runner(last_proof, next_proof, player_name):
    print(f'initializing runner {player_name}')
    player = Player(player_name)
    player.last_proof()
    last_proof.value = player.get_last_proof()
    while True:
        player.traverse(player.get_well_room())
        player.examine()
        player.traverse(player.get_mining_room())
        print(f'{player.name} is waiting for proof...')
        while next_proof.value is 0:
            time.sleep(1)
        while True:
            proof = next_proof.value
            print(f'{player.name} is sending proof {proof}.')
            next_proof.value = 0
            res = player.send_proof(proof)
            if len(res['errors']) == 0:
                print(f'{player.name.upper()} MINED A COIN -- TOTAL: {player.coins}')
                pusher_client.trigger('my-channel', 'my-event', {'message': f'{player.name.upper()} MINED A COIN -- TOTAL: {player.coins}'})
                player.last_proof()
                last_proof.value = player.get_last_proof()
                break
            if 'errors' in res and res['errors'][0] == 'There is no coin here: +100s':
                print(f'!!!WRONG MINING ROOM!!!')
                break

def snitch(mining_room, player_name):
    print('snitch')

def main(status):
    if status == "return":
        # Forces computer to shutdown
        shutdown(force = True)

    print('-------STARTING SCRIPT-------')
    players = [('carlos', miner), ('mike', runner),('dustin', runner),('miguel', runner),('doug', runner)]
    processes = {}
    last_proof = mp.Value('i', 0)
    next_proof = mp.Value('i', 0)
    n = 0

    for player in players:
        instance = player[1]
        p = mp.Process(target=instance, args=(last_proof, next_proof, player[0]))
        p.start()   
        processes[n] = {'process': p, 'player': player[0], 'instance': instance}
        n += 1

    while True:
        time.sleep(1)
        for p in list(processes.items()):
            pid = p[0]
            p = p[1]
            if not p['process'].is_alive():
                del processes[pid]
                process = mp.Process(target=p['instance'], args=(last_proof, next_proof, p['player']))
                process.start()
                processes[pid] = {'process': process, 'player': p['player'], 'instance': p['instance']}
        
# if __name__ == '__main__':
#     # freeze_support() here if program needs to be frozen
#     main()  # execute this only when run directly, not when imported!