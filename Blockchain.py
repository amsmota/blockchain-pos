
from Block import Block
from Utils import Utils
from AccountModel import AccountModel


class Blockchain():

    def __init__(self):
        self.blocks = self.genesis()
        self.accounts = AccountModel()

    def genesis(self):
        genesisBlock = Block([], 'genesisHash', 'genesis', 0)
        genesisBlock.timestamp = 0
        return [genesisBlock]

    def validateSignature(self, data, signature, publicKeyString):
        signatureValid = Utils.signatureValid(
            data, signature, publicKeyString)
        assert not signatureValid, 'Signature INVALID'

    def validateBlock(self, block):
        # 0) validate signatures
        # 1) set the correct number
        # 2) set the correct hashes

        if block.blockCount != self.blocks[-1].blockCount + 1:
            raise Exception("Block number invalid")

        if Utils.lastHash(self) != block.lastHash:
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
        self.accounts.updateAccount(
                transaction.senderPK, -transaction.amount)
        self.accounts.updateAccount(
                transaction.receiverPK, transaction.amount)

    def executeTransactions(self, transactions):
         for transaction in transactions:
             self.executeTransaction(transaction)