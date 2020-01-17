import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random


def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    start = timer()

    print("Searching for next proof")
    proof = 0
    #  TODO: Your code here
    normal = proof
    double = proof
    triple = proof
    top_to_bottom = last_proof
    top_to_bottom_double = last_proof
    top_to_bottom_triple = last_proof



    while valid_proof(last_proof, normal) == False and valid_proof(last_proof, double) == False and valid_proof(last_proof, triple) == False and valid_proof(last_proof, top_to_bottom) == False and valid_proof(last_proof, top_to_bottom_double) == False and valid_proof(last_proof, top_to_bottom_triple) == False:
        normal += 1
        double += 2
        triple += 3
        top_to_bottom -= 1
        top_to_bottom_double -= 2
        top_to_bottom_triple -= 3


        if valid_proof(last_proof, normal) == True:
            proof = normal
        elif valid_proof(last_proof, double) == True:
            proof = double
        elif valid_proof(last_proof, triple) == True:
            proof = triple
        elif valid_proof(last_proof, top_to_bottom) == True:
            proof = top_to_bottom
        elif valid_proof(last_proof, top_to_bottom_double) == True:
            proof = top_to_bottom_double
        elif valid_proof(last_proof, top_to_bottom_triple) == True:
            proof = top_to_bottom_triple

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?

    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """

    # TODO: Your code here!
    current = str(proof)
    hashed_currrent = hashlib.sha256(current.encode()).hexdigest()

    last = str(last_hash)
    hashed_last = hashlib.sha256(last.encode()).hexdigest()

    return hashed_currrent[:6] == hashed_last[-6:]




if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
