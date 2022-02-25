import threading
import time
from Message import Message
from BlockchainUtils import BlockchainUtils

class PeerDiscovery():

    def __init__(self, node):
        self.socketCommunication = node # it's a instance of SocketCommunication

    def start(self):
        statusThread = threading.Thread(target=self.status, args=[])
        statusThread.start()
        discoveryThread = threading.Thread(target=self.discovery, args=[])
        discoveryThread.start()

    def status(self):
        while True:
            print('Current Connections:')
            for peer in self.socketCommunication.peers:
                print('   ' + str(peer.ip) + ':' + str(peer.port))
            time.sleep(10)

    def discovery(self):
        while True:
            handshakeMessage = self.handshakeMessage()
            self.socketCommunication.broadcast(handshakeMessage)
            time.sleep(10)

    def handshake(self, node):
        self.socketCommunication.send(node, self.handshakeMessage())

    def handshakeMessage(self):
        connector = self.socketCommunication.socketConnector
        peers = self.socketCommunication.peers
        data = peers
        type = 'DISCOVERY'
        message = Message(connector, type, data)
        encodedMessage = BlockchainUtils.encode(message)
        return encodedMessage

    def handleMessage(self, message):
        peerConnector = message.connector
        peersPeerList = message.data
        newPeer = True
        for peer in self.socketCommunication.peers:
            if peer.equals(peerConnector):
                newPeer = False
        if newPeer:
            self.socketCommunication.peers.append(peerConnector)

        for peersPeer in peersPeerList:
            knownPeer = False
            for peer in self.socketCommunication.peers:
                if peer.equals(peersPeer):
                    knownPeer = True
            if not knownPeer and not peersPeer.equals(self.socketCommunication.socketConnector):
                self.socketCommunication.connect_with_node(peersPeer.ip, peersPeer.port)

