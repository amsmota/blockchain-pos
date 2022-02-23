from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

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
        dataHash = hash(data)
        publicKey = RSA.importKey(publicKeyString)
        signatureSchemaObject = PKCS1_v1_5.new(publicKey)
        signatureValid = signatureSchemaObject.verify(dataHash, signature)
        return signatureValid

    @staticmethod
    def lastHash(blockchain):
        return hash(blockchain.blocks[-1].payload()).hexdigest()

    @staticmethod
    def blockCount(blockchain):
        return blockchain.blocks[-1].blockCount + 1

    @staticmethod
    def encode(data):
        return jsonpickle.encode(data, unpicklable=True)

    @staticmethod
    def decode(data):
        return jsonpickle.decode(data)

