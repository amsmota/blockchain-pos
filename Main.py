from BlockchainNode import BlockchainNode
import sys


if __name__ == '__main__':

    # argv[0] is the name of the program
    ip = sys.argv[1] 
    port = int(sys.argv[2])
    apiPort = int(sys.argv[3])

    keyFile = None
    if len(sys.argv) > 4:
        keyFile = sys.argv[4]     

    node = BlockchainNode(ip, port, keyFile)
    node.startP2P()
    node.startAPI(apiPort)
