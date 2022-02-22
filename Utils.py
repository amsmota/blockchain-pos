from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import json
import pprint


class Utils():

    @staticmethod
    def pprint(data):
        pprint.pprint(data)

    @staticmethod
    def jprint(data):
        pprint.pprint(json.dumps(data))

    @staticmethod
    def hash(data):
        dataString = json.dumps(data)
        dataBytes = dataString.encode('utf8')
        dataHash = SHA256.new(dataBytes)
        return dataHash
        
    @staticmethod
    def signatureValid(data, signature, publicKeyString):
        signature = bytes.fromhex(signature)
        dataHash = Utils.hash(data)
        publicKey = RSA.importKey(publicKeyString)
        signatureSchemaObject = PKCS1_v1_5.new(publicKey)
        signatureValid = signatureSchemaObject.verify(dataHash, signature)
        return signatureValid

    @staticmethod
    def lastHash(blockchain):
        return Utils.hash(blockchain.blocks[-1].payload()).hexdigest()

    @staticmethod
    def blockCount(blockchain):
        return blockchain.blocks[-1].blockCount + 1
