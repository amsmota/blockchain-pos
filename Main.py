from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain

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

    pprint.pprint(blockchain.toJson())
    pprint.pprint('===========================')

    block = wallet.createBlock(pool.transactions, blockchain.lastBlockHash, blockchain.lastBlockNumber+1)

    # signatureValid = Wallet.signatureValid(
    #     block.payload(), block.signature, wallet.publicKeyString())
    # assert signatureValid, 'Wallet signature OK'

    # signatureInvalid = Wallet.signatureValid(
    #     block.payload(), block.signature, fraudWallet.publicKeyString())
    # assert not signatureInvalid, 'Fraud signature failed'

   
    blockchain.addBlock(block)

    pprint.pprint(blockchain.toJson())
