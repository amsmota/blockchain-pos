from Node import Node
from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
from Utils import Utils
from AccountModel import AccountModel

import sys
import pprint

if __name__ == '__main__':

    # argv[0] is the name of the program
    ip = sys.argv[1] 
    port = int(sys.argv[2])

    node = Node(ip, port)
    node.startP2P()






