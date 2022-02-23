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

