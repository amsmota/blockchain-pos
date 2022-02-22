import uuid
import time
import copy

class Transaction():

    def __init__(self, senderPK, receiverPK, amount, type) -> None:
        self.senderPK = senderPK
        self.receiverPK = receiverPK
        self.amount = amount
        self.type = type
        self.id = uuid.uuid1().hex
        self.timestamp = time.time()
        self.signature = ''

    def toJson(self):
        return self.__dict__

    def sign(self, signature):
        self.signature = signature

    def payload(self):
        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonRepresentation['signature'] = ''
        return jsonRepresentation

    def equals(self, transaction):
        return self.id == transaction.id



