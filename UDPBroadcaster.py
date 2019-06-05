import socket
import time
import random
import chatModule
import io

broadcastMessage = "let's chat"
broadcastListenPort = 12345
broadcastPort = random.randint(1024, 65535)
broadcastIP = "255.255.255.255"
broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcastSocket.bind(('', broadcastPort))
broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcastSocket.setblocking(False)

def broadcastListen(stopBListen):
    broadcastListenSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcastListenSocket.bind(('', broadcastListenPort))
    print("Listening to broadcasts")
    while not stopBListen.is_set():
        message , peerAddress =broadcastListenSocket.recvfrom(1024)
        message = message.decode('UTF-8')
        #print(message + "  " + str(peerAddress))
        if message == "let's chat" and (peerAddress not in chatModule.broadcastPeers) and peerAddress[1] != broadcastPort:
            print("Found peer!")
            chatModule.broadcastPeers.append(peerAddress)
            serverPort = random.randint(1024, 65535)
            tempSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            tempSocket.sendto(("ok "+str(serverPort)).encode('UTF-8'), peerAddress)
            chatModule.setupChatServer(serverPort)
    print("Listening to broadcasts stopped")

def broadcast(stopBroadcast):
    print("Broadcast started")
    while not stopBroadcast.is_set():
        broadcastSocket.sendto(broadcastMessage.encode('UTF-8'), (broadcastIP, broadcastListenPort))
        try:
            message, peerAddress = broadcastSocket.recvfrom(1024)
            message = message.decode('UTF-8')
            #print(message + "  " + str(peerAddress))
            if message.split()[0] == 'ok':
                print("Found peer!")
                chatModule.broadcastPeers.append(peerAddress)
                connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connection.connect((peerAddress[0], int(message.split()[1])))
                chatModule.setupChatClient(connection)
        except io.BlockingIOError:
            pass
        time.sleep(1)
    print("Broadcast stopped")

