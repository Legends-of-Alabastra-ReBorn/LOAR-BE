import hashlib

import sys
from timeit import default_timer as timer
import random


def proof_of_work(last_proof, difficulty):
    print("Searching for next proof...")
    start = timer()
    proof = 80000000
    total_tries = 0
    # prev_proof = f'{last_proof}'.encode()
    while valid_proof(last_proof, proof, difficulty) is False:
        proof = random.randint(0, 100000000)
        total_tries += 1
        if total_tries % 1000000 == 0:
            print(total_tries/1000000,'million tries')
    
    if valid_proof(last_proof, proof, difficulty):
        print("Proof found: " + str(proof) + " in " + str(timer() - start))

def valid_proof(last_proof, proof, difficulty):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:difficulty] == "0" * difficulty

LAST_PROOF = 48142522
DIFFICULTY = 6

print(proof_of_work(LAST_PROOF, DIFFICULTY))