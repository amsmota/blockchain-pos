from Crypto.Hash import SHA256
import json


class Utils():

    @staticmethod
    def hash(data):
        dataString = json.dumps(data)
        dataBytes = dataString.encode('utf8')
        dataHash = SHA256.new(dataBytes)
        return dataHash
        