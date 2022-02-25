
from Block import Block
from BlockchainUtils import BlockchainUtils
from ProofOfStake import ProofOfStake
from AccountModel import AccountModel
class Blockchain():

    def __init__(self):
        self.blocks = self.genesis()
        self.accounts = AccountModel()
        self.pos = ProofOfStake()

    def genesis(self):
        genesisBlock = Block([], 'genesisHash', 'genesis', 0)
        genesisBlock.timestamp = 0
        return [genesisBlock]

    def validateSignature(self, data, signature, publicKeyString):
        signatureValid = BlockchainUtils.signatureValid(
            data, signature, publicKeyString)
        assert not signatureValid, 'Signature INVALID'

    def validateBlock(self, block):
        # 1) validate the correct number
        # 2) validate the correct hashes
        # 3) validate signatures
        if block.blockCount != self.blocks[-1].blockCount + 1:
            raise Exception("Block number invalid")

        if BlockchainUtils.lastHash(self) != block.lastHash:
            raise Exception("Block hash invalid")

        for transaction in block.transactions:
            self.validateSignature(
                transaction.toJson(), transaction.signature, transaction.senderPK)
            self.validateSignature(
                transaction.toJson(), transaction.signature, transaction.receiverPK)

    def addBlock(self, block):
        # update accounts
        self.executeTransactions(block.transactions)
        # add to blockchain
        self.blocks.append(block)

    def toJson(self):
        data = {}
        jsonBlocks = []
        for block in self.blocks:
            jsonBlocks.append(block.toJson())
        data['blocks'] = jsonBlocks
        return data

    def transactionsCovered(self, transaction):
        if transaction.type == 'EXCHANGE':
            return True
        senderBalance = self.accounts.getbalance(transaction.senderPK)
        return senderBalance >= transaction.amount

    def getCoveredTransactions(self, transactions):
        coveredTransactions = []
        for transaction in transactions:
            if self.transactionsCovered(transaction):
                coveredTransactions.append(transaction)
            else:
                raise Exception("Transaction not covered by the Sender")
            return coveredTransactions

    def executeTransaction(self, transaction):
        senderPK = transaction.senderPK
        receiverPK = transaction.receiverPK
        amount = transaction.amount
        if transaction.type == 'STAKE':
            if senderPK == receiverPK:
                self.pos.update(senderPK, amount)
                self.accounts.updateAccount(senderPK, -amount)
        else:
            self.accounts.updateAccount(senderPK, -amount)
            self.accounts.updateAccount(receiverPK, amount)

    def executeTransactions(self, transactions):
        for transaction in transactions:
            self.executeTransaction(transaction)

    def nextForger(self):
        lastBlockHash = BlockchainUtils.hash(
            self.blocks[-1].payload()).hexdigest()
        nextForger = self.pos.forger(lastBlockHash)
        return nextForger
