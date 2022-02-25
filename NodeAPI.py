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

    @route('/info', methods=['GET'])
    def info(self):
        return "info", 200

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
        blockNode.incomingTransaction(transaction)
        response = {'message': 'Received transaction'}
        return jsonify(response), 201
