


class TransactionPool():

    def __init__(self):
        self.transactions = []

    def addTransaction(self, transaction):
        self.transactions .append(transaction)

    def transactionExists(self, transaction):
        for poolTransaction in self.transactions:
            if poolTransaction.equals(transaction):
                return True
        return False

    def removeTransactions(self, transactions):
        for transaction in transactions:
            self.transactions.remove(transaction)
            
    def forgerRequired(self):
        return len(self.transactions) >= 2

