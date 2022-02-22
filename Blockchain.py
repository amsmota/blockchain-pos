
from Block import Block
from Utils import Utils


class Blockchain():

    def __init__(self):
        self.blocks = self.genesis()

    def genesis(self):
        genesisBlock = Block([], 'genesisHash', 'genesis', 0)
        genesisBlock.timestamp = 0
        return [genesisBlock]

    def validateSignature(self, data, signature, publicKeyString):
        signatureValid = Utils.signatureValid(
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

        if block.blockCount != self.blocks[-1].blockCount +1:
            raise Exception("Block number invalid")

        if Utils.lastHash(self) != block.lastHash:
            raise Exception("Block hash invalid")

        self.blocks.append(block)

    def toJson(self):
        data = {}
        jsonBlocks = []
        for block in self.blocks:
            jsonBlocks.append(block.toJson())
        data['blocks'] = jsonBlocks
        return data
