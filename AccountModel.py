


class AccountModel():

    def __init__(self):
        self.accounts = {}

    def addAccount(self, pkString, value):
        if not pkString in self.accounts:
            self.accounts[pkString] = value

    def updateAccount(self, pkString, value):
        self.accounts[pkString] += value 

    def getbalance(self, pkString):
        return self.accounts[pkString]

