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
        proof = random.randint(0, sys.maxsize)
        total_tries += 1
        if total_tries % 1000000 == 0:
            print(total_tries/1000000,'million tries')
    if valid_proof(last_proof, proof, difficulty):
        return proof

def Decipher_Clue(clue):
    cpu = CPU()
    cpu.load(clue)
    return cpu.run()