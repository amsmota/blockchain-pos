from Wallet import Wallet
from Utils import Utils

import copy


class Blockchain():

    def __init__(self):
        self.wallet = Wallet()
        self.blocks = self.genesis()
        self.lastBlockNumber = 0
        self.lastBlockHash = str(self.blocks[0].lastHash)

    def genesis(self):
        transactions = []
        transaction = self.wallet.createTransaction(
            self.wallet.publicKeyString(), 0, 'GENESIS')
        transactions.append(transaction)
        block = self.wallet.createBlock(
            transactions, Utils.hash(transaction.toJson()).hexdigest(), 0)

        self.validateSignature(
            transaction.toJson(), transaction.signature, transaction.receiverPK)

        blocks = []
        blocks.append(block)
        return blocks

    def validateSignature(self, data, signature, publicKeyString):
        print(publicKeyString)
        signatureValid = Wallet.signatureValid(
            data, signature, publicKeyString)
        assert not signatureValid, 'Signature INVALID'

    def addBlock(self, block):
        # 0) validate signatures
        # 1) set the correct number
        # 2) set the correct hashes
        for transaction in block.transactions:
            self.validateSignature(
                transaction.toJson(), transaction.signature, transaction.senderPK)
            self.validateSignature(
                transaction.toJson(), transaction.signature, transaction.receiverPK)

        if block.blockCount <= self.lastBlockNumber:
            raise Exception("Block number invalid")

        if block.lastHash != self.lastBlockHash:
            raise Exception("Block hash invalid")

        self.blocks.append(block)
        self.lastBlockNumber = block.blockCount
        self.lastBlockHash = block.lastHash

    def toJson(self):
        data = {}
        data['lastBlockNumber'] = self.lastBlockNumber
        data['lastBlockHash'] = self.lastBlockHash
        jsonBlocks = []
        for block in self.blocks:
            jsonBlocks.append(block.toJson())
        data['blocks'] = jsonBlocks
        return data
