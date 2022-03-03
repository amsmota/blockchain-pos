from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Message import Message

import json
import jsonpickle

class BlockchainUtils():

    @staticmethod
    def hash(data):
        dataString = json.dumps(data)
        dataBytes = dataString.encode('utf8')
        dataHash = SHA256.new(dataBytes)
        return dataHash
        
    @staticmethod
    def signatureValid(data, signature, publicKeyString):
        signature = bytes.fromhex(signature)
        dataHash = BlockchainUtils.hash(data)
        publicKey = RSA.importKey(publicKeyString)
        signatureSchemaObject = PKCS1_v1_5.new(publicKey)
        signatureValid = signatureSchemaObject.verify(dataHash, signature)
        return signatureValid

    @staticmethod
    def lastBlockHash(blockchain):
        return BlockchainUtils.hash(blockchain.blocks[-1].payload()).hexdigest()

    @staticmethod
    def newBlockNumber(blockchain):
        return blockchain.blocks[-1].blockCount + 1

    @staticmethod
    def encode(data):
        return jsonpickle.encode(data, unpicklable=True)

    @staticmethod
    def decode(data):
        return jsonpickle.decode(data)

    @staticmethod
    def createEncodedMessage(connector, type, data):
         message = Message(connector, type, data)
         message = BlockchainUtils.encode(message)
         return message

    @staticmethod
    def broadcastMessage(p2p, type, data):
         message = Message(p2p.socketConnector, type, data)
         message = BlockchainUtils.encode(message)
         p2p.broadcast(message)

