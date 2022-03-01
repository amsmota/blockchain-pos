from Blockchain import Blockchain
from NodeAPI import NodeAPI
from SocketCommunication import SocketCommunication
from TransactionPool import TransactionPool
from Wallet import Wallet
from BlockchainUtils import BlockchainUtils


class BlockchainNode():

    def __init__(self, ip, port, key=None):
        self.p2p = None
        self.ip = ip
        self.port = port
        self.blockchain = Blockchain()
        self.transactionPool = TransactionPool()
        self.wallet = Wallet()
        if key:
            self.wallet.fromKey(key)

    def startP2P(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.startSocketCommunication(self)

    def startAPI(self, apiPort):
        self.api = NodeAPI()
        self.api.injectNode(self)
        self.api.start(apiPort)

    def incomingTransaction(self, transaction):
        validSignature = BlockchainUtils.signatureValid(
            transaction.payload(), transaction.signature, transaction.senderPK)
        transactionInPool = self.transactionPool.transactionExists(transaction)
        transactionInBlock = self.blockchain.transactionExists(transaction)
        if not transactionInPool and validSignature and not transactionInBlock:
            self.transactionPool.addTransaction(transaction)
            encodedMessage = BlockchainUtils.createEncodedMessage(
                self.p2p.socketConnector, 'TRANSACTION', transaction)
            self.p2p.broadcast(encodedMessage)
            # New block?
            forgingRequired = self.transactionPool.forgerRequired()
            if forgingRequired:
                self.forge()

    def forge(self):
        forger = self.blockchain.nextForger()
        if forger == self.wallet.publicKeyString():
            block = self.blockchain.createBlock(
                self.transactionPool.transactions, self.wallet)
            self.transactionPool.removeTransactions(block.transactions)
            encodedMessage = BlockchainUtils.createEncodedMessage(
                self.p2p.socketConnector, 'BLOCK', block)
            self.p2p.broadcast(encodedMessage)
            print("I'm the Forger that created block " + str(block.blockCount))
        else:
            print("I'm NOT a forger")

    def addBlock(self, block):
        self.blockchain.addBlock(block)
        self.transactionPool.removeTransactions(block.transactions)

