from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
from Utils import Utils
from AccountModel import AccountModel

import pprint

if __name__ == '__main__':

    blockchain = Blockchain()
    
    alice = Wallet()
    bob = Wallet()
    exchange = Wallet()
    forger = Wallet()

    transaction = exchange.createTransaction(alice.publicKeyString(), 50, 'EXCHANGE')
    pool = TransactionPool()
    pool.addTransaction(transaction)
    coveredecTransactions = blockchain.getCoveredTransactions(pool.transactions)
    block = forger.createBlock(coveredecTransactions, Utils.lastHash(blockchain), Utils.blockCount(blockchain))
    blockchain.validateBlock(block)
    blockchain.addBlock(block)

    transaction = alice.createTransaction(bob.publicKeyString(), 50, 'TRANSFER')
    pool = TransactionPool()
    pool.addTransaction(transaction)
    coveredecTransactions = blockchain.getCoveredTransactions(pool.transactions)
    block = forger.createBlock(coveredecTransactions, Utils.lastHash(blockchain), Utils.blockCount(blockchain))
    blockchain.validateBlock(block)
    blockchain.addBlock(block)

    pprint.pprint(blockchain.toJson())
    pprint.pprint(blockchain.accounts.accounts)


