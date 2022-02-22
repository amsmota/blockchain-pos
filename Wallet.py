from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Utils import Utils
from Transaction import Transaction
from Block import Block

class Wallet():

    def __init__(self):
        self.keyPair = RSA.generate(2048)

    def sign(self, data):
        dataHash = Utils.hash(data)
        signatureSchemaObject = PKCS1_v1_5.new(self.keyPair)
        signature = signatureSchemaObject.sign(dataHash)
        return signature.hex()

    @staticmethod
    def signatureValid(data, signature, publicKeyString):
        signature = bytes.fromhex(signature)
        dataHash = Utils.hash(data)
        publicKey = RSA.importKey(publicKeyString)
        signatureSchemaObject = PKCS1_v1_5.new(publicKey)
        signatureValid = signatureSchemaObject.verify(dataHash, signature)
        return signatureValid

    def publicKeyString(self):
        publicKeyString = self.keyPair.publickey().exportKey('PEM').decode('utf-8')
        return publicKeyString
    
    def createTransaction(self, receiver, amount, type):
        transaction = Transaction(self.publicKeyString(), receiver, amount, type)
        signature = self.sign(transaction.payload())
        transaction.sign(signature)
        return transaction

    def createBlock(self, transactions, lastHash, blockCount):
        block = Block(transactions, lastHash, self.publicKeyString(), blockCount)
        signature = self.sign(block.payload())
        block.sign(signature)
        return block




        
