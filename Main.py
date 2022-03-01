from BlockchainNode import BlockchainNode
import sys
from Wallet import Wallet
import debugpy


if __name__ == '__main__':

    dport = sys.argv[-1]
    if dport.startswith('--debug'):
        dport = dport[8:12]
        debugpy.listen(int(dport))
        print("Debugger listening on port: " + dport)
        debugpy.wait_for_client()
        debugpy.breakpoint()
    else:
        dport = None

    # argv[0] is the name of the program
    ip = sys.argv[1]
    port = int(sys.argv[2])
    apiPort = int(sys.argv[3])

    keyFile = None
    if len(sys.argv) > 4 and not sys.argv[4].startswith('--debug'):
        keyFile = sys.argv[4]
        print(keyFile)

    node = BlockchainNode(ip, port, keyFile)
    node.startP2P()
    # give the man some money
    exchange = Wallet()
    transaction = exchange.createTransaction(
        node.wallet.publicKeyString(), 1000, 'EXCHANGE')
    node.incomingTransaction(transaction)

    node.startAPI(apiPort)

