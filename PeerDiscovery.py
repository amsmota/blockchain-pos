from BlockchainUtils import BlockchainUtils

import threading
import time


class PeerDiscovery():

    def __init__(self, socketCommunication):
        self.p2p = socketCommunication

    def start(self):
        statusThread = threading.Thread(target=self.status, args=[])
        statusThread.start()
        discoveryThread = threading.Thread(target=self.discovery, args=[])
        discoveryThread.start()

    def status(self):
        while True:
            print('Current Connections:')
            for peer in self.p2p.peers:
                print('   ' + str(peer.ip) + ':' + str(peer.port))
            time.sleep(30)

    def discovery(self):
        while True:
            handshakeMessage = self.handshakeMessage()
            self.p2p.broadcast(handshakeMessage)
            time.sleep(10)

    def handshake(self, node):
        self.p2p.send(node, self.handshakeMessage())

    def handshakeMessage(self):
        encodedMessage = BlockchainUtils.createEncodedMessage(
                self.p2p.socketConnector, 'DISCOVERY', self.p2p.peers)
        return encodedMessage

    def handleMessage(self, message):
        peerConnector = message.connector
        peersPeerList = message.data
        newPeer = True
        for peer in self.p2p.peers:
            if peer.equals(peerConnector):
                newPeer = False
        if newPeer:
            print("Adding new node " + message.connector.ip+":"+ str(message.connector.port))
            self.p2p.peers.append(peerConnector)

        for peersPeer in peersPeerList:
            knownPeer = False
            for peer in self.p2p.peers:
                if peer.equals(peersPeer):
                    knownPeer = True
            if not knownPeer and not peersPeer.equals(self.p2p.socketConnector):
                print("Connecting to new node " + message.connector.ip+":"+ str(message.connector.port))
                self.p2p.connect_with_node(peersPeer.ip, peersPeer.port)

