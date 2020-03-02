import hashlib
import random
import sys

from cpu import CPU

def Mine(last_proof, difficulty):
    def valid_proof(last_proof, proof, difficulty):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:difficulty] == "0" * difficulty
    print(f'Searching for next proof with {last_proof}...')
    proof = 0
    total_tries = 0
    while valid_proof(last_proof, proof, difficulty) is False:
        # proof = random.randint(0, sys.maxsize)
        proof = random.randint(0, 2147483646)
        total_tries += 1
        if total_tries % 10000000 == 0:
            print(f'{int(total_tries/10000000)}0 million tries...')
    if valid_proof(last_proof, proof, difficulty):
        return proof

# def Decipher_Clue(clue):
#     cpu = CPU()
#     cpu.load(clue)
#     return cpu.run()

def Decipher_Clue(clue):
    return clue.split(' ')[-1]