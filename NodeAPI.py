from crypt import methods
from flask_classful import FlaskView, route
from flask import Flask, jsonify, request
from BlockchainUtils import BlockchainUtils

# global
blockNode = None


class NodeAPI(FlaskView):

    def __init__(self):
        self.app = Flask(__name__)

    def start(self, apiPort):
        NodeAPI.register(self.app, route_base='/')
        self.app.run(host='localhost', port=apiPort)

    def injectNode(self, node):
        global blockNode
        blockNode = node

    @route('/pool/limit/<limit>', methods=['GET'])
    def blocklimit(self, limit):
        limit = int(limit)
        blockNode.transactionPool.setBlockLimit(limit)
        return "Transaction Pool Limit set to "+str(limit), 200

    @route('/pkey', methods=['GET'])
    def pkey(self):
        return blockNode.wallet.publicKeyString(), 200

    @route('/accounts', methods=['GET'])
    def accounts(self):
        return blockNode.blockchain.accounts.accounts, 200

    @route('/stakes', methods=['GET'])
    def stakes(self):
        return blockNode.blockchain.pos.stakers, 200

    @route('/stakes/<amount>', methods=['GET'])
    def stake(self, amount):
        stake = int(amount)
        wallet = blockNode.wallet
        transaction = wallet.createTransaction(
            wallet.publicKeyString(), stake, 'STAKE')
        blockNode.handleTransaction(transaction)
        return blockNode.blockchain.pos.stakers, 200

    @route('/blockchain', methods=['GET'])
    def blockchain(self):
        return blockNode.blockchain.toJson(), 200

    @route('/transactions', methods=['GET'])
    def transactions(self):
        transactions = {}
        for ctr, transaction in enumerate(blockNode.transactionPool.transactions):
            transactions[ctr] = transaction.toJson()
        return jsonify(transactions), 200

    @route('/transaction', methods=['POST'])
    def transaction(self):
        values = request.get_json()
        if not 'transaction' in values:
            return "Missing transaction.", 400
        transaction = BlockchainUtils.decode(values['transaction'])
        blockNode.handleTransaction(transaction)
        response = {'message': 'Received transaction'}
        return jsonify(response), 201
