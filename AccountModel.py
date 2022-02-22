


class AccountModel():

    def __init__(self):
        self.accounts = {}

    def addAccount(self, pkString, value):
        if not pkString in self.accounts:
            self.accounts[pkString] = value

    def updateAccount(self, pkString, value):
        if not pkString in self.accounts:
            self.addAccount(pkString, 0)
        self.accounts[pkString] += value 

    def getbalance(self, pkString):
        if not pkString in self.accounts:
            self.addAccount(pkString, 0)
        return self.accounts[pkString]

