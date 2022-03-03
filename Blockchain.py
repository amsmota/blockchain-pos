
from Block import Block
from BlockchainUtils import BlockchainUtils
from ProofOfStake import ProofOfStake
from AccountModel import AccountModel


class Blockchain():

    def __init__(self):
        self.blocks = self.genesis()
        self.blockIds = {}
        self.accounts = AccountModel()
        self.pos = ProofOfStake()

    def genesis(self):
        genesisBlock = Block([], 'genesisHash', 'genesis', 0)
        genesisBlock.timestamp = 0
        return [genesisBlock]

    def addBlock(self, block):
        if self.blockIds.get(block.blockCount) != None:
            print("BLOCK INVALID!!!!!!!!!!!!!!!!!!!!!")
            return
        self.executeTransactions(block.transactions)  # update accounts too
        self.blocks.append(block)
        self.blockIds[block.blockCount] = block.forger

    def toJson(self):
        data = {}
        jsonBlocks = []
        for block in self.blocks:
            jsonBlocks.append(block.toJson())
        data['blocks'] = jsonBlocks
        return data

    def blockCountValid(self, block):
        return self.blocks[-1].blockCount == block.blockCount - 1

    def lastBlockHashValid(self, block):
        latestBlockchainBlockHash = BlockchainUtils.hash(
            self.blocks[-1].payload()).hexdigest()
        return latestBlockchainBlockHash == block.lastHash

    def getCoveredTransactions(self, transactions):
        coveredTransactions = []
        for transaction in transactions:
            if self.transactionsCovered(transaction):
                coveredTransactions.append(transaction)
            else:
                print("Transaction not covered by the Sender")
        return coveredTransactions

    def transactionsCovered(self, transaction):
        if transaction.type == 'EXCHANGE':
            return True
        senderBalance = self.accounts.getbalance(transaction.senderPK)
        return senderBalance >= transaction.amount

    def executeTransactions(self, transactions):
        for transaction in transactions:
            self.executeTransaction(transaction)

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

    def nextForger(self):
        lastBlockHash = BlockchainUtils.hash(
            self.blocks[-1].payload()).hexdigest()
        nextForger = self.pos.forger(lastBlockHash)
        return nextForger

    def createBlock(self, transactions, forgerWallet):
        coveredTransactions = self.getCoveredTransactions(transactions)
        self.executeTransactions(coveredTransactions)
        newBlock = forgerWallet.createBlock(coveredTransactions, BlockchainUtils.lastBlockHash(
            self), len(self.blocks)) #BlockchainUtils.newBlockNumber(self))
        self.blocks.append(newBlock)
        return newBlock

    def transactionExists(self, transaction):
        for block in self.blocks:
            for blockTransaction in block.transactions:
                if transaction.equals(blockTransaction):
                    return True
        return False

    def forgerValid(self, block):
        forgerPublicKey = self.pos.forger(block.lastHash)
        proposedBlockForger = block.forger
        if forgerPublicKey == proposedBlockForger:
            return True
        else:
            return False

    def transactionsValid(self, transactions):
        coveredTransactions = self.getCoveredTransactions(transactions)
        if len(coveredTransactions) == len(transactions):
            return True
        return False

    def validateSignature(self, data, signature, publicKeyString):
        signatureValid = BlockchainUtils.signatureValid(
            data, signature, publicKeyString)
        return signatureValid
    def validateBlock(self, block):
        # 1) validate the correct block number
        # 2) validate the correct block hashes
        # 3) validate the correct block forger
        # 4) validate the block signature
        # 5) validate the transactions
        # 6) validate the transactions signatures

        # if block.blockCount != self.blocks[-1].blockCount + 1:
        #     raise Exception("Block number INVALID")

        # if BlockchainUtils.lastBlockHash(self) != block.lastHash:
        #     raise Exception("Block hash INVALID")

        forgerPublicKey = self.pos.forger(block.lastHash)  # ?????
        proposedBlockForger = block.forger
        if forgerPublicKey != proposedBlockForger:
            raise Exception("Forger INVALID")

        self.validateSignature(
            block.payload(), block.signature, block.forger)

        coveredTransactions = self.getCoveredTransactions(block.transactions)
        if len(coveredTransactions) != len(block.transactions):
            raise Exception("Transactions INVALID")

        for transaction in block.transactions:
            self.validateSignature(
                transaction.toJson(), transaction.signature, transaction.senderPK)
            self.validateSignature(
                transaction.toJson(), transaction.signature, transaction.receiverPK)

        return True
