from ProofOfStake import ProofOfStake
from Lot import Lot
import string
import random

def getRandomString(lenght):
    letters = string.ascii_lowercase
    result = ''.join(random.choice(letters) for i in range(lenght))
    return result



if __name__ == '__main__':

    pos = ProofOfStake()
    pos.update('bob', 100)
    pos.update('alice', 100)

    bobWins = 0
    aliceWins = 0

    for i in range(100):
        forger = pos.forger(getRandomString(i))
        if forger == 'bob':
            bobWins += 1
        elif forger == 'alice':
            aliceWins += 1

    print ('bob wins: ' + str(bobWins))
    print ('alice wins: ' + str(aliceWins))

