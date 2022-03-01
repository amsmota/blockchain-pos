import copy
from Blockchain import Blockchain
from Message import Message
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

    def handleTransaction(self, transaction):
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

    # def handleBlock(self, block):
    #     blockCountValid = self.blockchain.blockCountValid(block)
    #     if not blockCountValid:
    #         self.requestChain()

    #     # self.blockchain.validateBlock(block)
    #     self.blockchain.addBlock(block)
    #     self.transactionPool.removeTransactions(block.transactions)
    #     message = BlockchainUtils.createEncodedMessage(self.p2p.socketConnector, 'BLOCK', block)
    #     self.p2p.broadcast(message)

    def handleBlock(self, block):
        forger = block.forger
        blockHash = block.payload()
        signature = block.signature

        blockCountValid = self.blockchain.blockCountValid(block)
        lastBlockHashValid = self.blockchain.lastBlockHashValid(block)
        forgerValid = self.blockchain.forgerValid(block)
        transactionsValid = self.blockchain.transactionsValid(
            block.transactions)
        signatureValid = BlockchainUtils.signatureValid(blockHash, signature, forger)
        if not blockCountValid:
            self.requestChain()
        if lastBlockHashValid and forgerValid and transactionsValid and signatureValid:
            self.blockchain.addBlock(block)
            self.transactionPool.removeTransactions(block.transactions)
            message = Message(self.p2p.socketConnector, 'BLOCK', block)
            self.p2p.broadcast(BlockchainUtils.encode(message))

    def requestChain(self):
        message = BlockchainUtils.createEncodedMessage(self.p2p.socketConnector, 'BLOCKCHAINREQUEST', None)
        self.p2p.broadcast(message)

    def handleBlockchainRequest(self, node):
        message = BlockchainUtils.createEncodedMessage(self.p2p.socketConnector, 'BLOCKCHAINUPDATE', self.blockchain)
        self.p2p.send(node, message)

    def handleBlockchainUpdate(self, receivedBlockchain):
        localBlockchainCopy = copy.deepcopy(self.blockchain)
        localBlockchainCount = len(localBlockchainCopy.blocks)
        receivedBlockchainCount = len(receivedBlockchain.blocks)
        if localBlockchainCount < receivedBlockchainCount:
            for blockNumber, block in enumerate(receivedBlockchain.blocks):
                if blockNumber >= localBlockchainCount:
                    localBlockchainCopy.addBlock(block)
                    self.transactionPool.removeTransactions(block.transactions)
            self.blockchain = localBlockchainCopy

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
