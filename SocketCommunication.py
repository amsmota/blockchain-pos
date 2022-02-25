from p2pnetwork.node import Node
from BlockchainUtils import BlockchainUtils
from PeerDiscovery import PeerDiscovery
from SocketConnector import SocketConnector

import json

### Indicate methods from p2pnetwork.node.Node

class SocketCommunication(Node): ### extends p2pnetwork.node.Node

    def __init__(self, ip, port):
        super(SocketCommunication, self).__init__(ip, port, None) # None is a callback
        self.peers = []
        self.peerDiscovery = PeerDiscovery(self)
        self.socketConnector = SocketConnector(ip, port)
        self.mainNodePort = 10001

    def startSocketCommunication(self, blockchainNode):
         ### Start the thread's activity (in p2pnetwork.node.Node)
        self.blockchainNode = blockchainNode
        self.start()
        self.peerDiscovery.start()
        self.connectToMaintNode()

    def connectToMaintNode(self):
        if self.socketConnector.port != self.mainNodePort:
            ### Make a connection with another node that is running on host with port.
            self.connect_with_node('localhost', self.mainNodePort) 

    def send(self, receiver, message):
        ### Send the data to the receiver node if it exists.
        self.send_to_node(receiver, message) 

    def broadcast(self, message):
        ### Send a message to all the nodes that are connected with this node.
        self.send_to_nodes(message) 
    
    ### This method is invoked when a node successfully connected with us.
    def inbound_node_connected(self, node):
        self.peerDiscovery.handshake(node)
    
    ### This method is invoked when a connection with a outbound node was successfull.
    def outbound_node_connected(self, node):
        self.peerDiscovery.handshake(node)

    ### This method is invoked when a node send us a message.
    def node_message(self, node, data):
        message = BlockchainUtils.decode(json.dumps(data))
        if message.messageType == 'DISCOVERY':
            self.peerDiscovery.handleMessage(message)
        elif message.messageType == 'TRANSACTION':
            transaction = message.data
            self.blockchainNode.incomingTransaction(transaction)
