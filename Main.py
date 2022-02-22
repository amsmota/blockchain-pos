from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
from Utils import Utils
from AccountModel import AccountModel

import pprint

if __name__ == '__main__':

    accountModel = AccountModel()
    wallet = Wallet()

    accountModel.addAccount(wallet.publicKeyString(), 100)

    accountModel.updateAccount(wallet.publicKeyString(), 10)

    pprint.pprint(accountModel.accounts)


