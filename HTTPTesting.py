from urllib import request
from Wallet import Wallet
from BlockchainUtils import BlockchainUtils
import requests

if __name__ == '__main__':

    alice = Wallet()
    bob = Wallet()
    exchange = Wallet()

    transaction = exchange.createTransaction(
        alice.publicKeyString(), 100, 'EXCHANGE')

    url = 'http://localhost:5000/transaction'
    package = {'transaction': BlockchainUtils.encode(transaction)}
    request = requests.post(url, json=package)
    print(request.text)

    transaction = alice.createTransaction(
        bob.publicKeyString(), 10, 'TRANSACTION')

    url = 'http://localhost:5001/transaction'
    package = {'transaction': BlockchainUtils.encode(transaction)}
    request = requests.post(url, json=package)
    print(request.text)

