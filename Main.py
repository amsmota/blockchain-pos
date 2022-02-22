from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
from Utils import Utils

import pprint

if __name__ == '__main__':

    amount = 1
    type = 'TRANSFER'

    wallet = Wallet()
    fraudWallet = Wallet()

    pool = TransactionPool()

    transaction = wallet.createTransaction(fraudWallet.publicKeyString(), amount, type)

    if not pool.transactionExists(transaction):
        pool.addTransaction(transaction)

    blockchain = Blockchain()

    block = wallet.createBlock(pool.transactions, Utils.lastHash(blockchain), Utils.blockCount(blockchain))
    blockchain.addBlock(block)

    block = wallet.createBlock(pool.transactions, Utils.lastHash(blockchain), Utils.blockCount(blockchain))
    blockchain.addBlock(block)

    pprint.pprint(blockchain.toJson())
