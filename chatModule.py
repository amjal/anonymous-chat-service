import queue
import socket
import threading
import time

keepConnection = True
tobesentMessages = queue.Queue(100)
chatPeers = []
broadcastPeers = []

def setupChatServer(serverPort):
    global keepConnection
    keepConnection = True
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    with serverSocket:
        serverSocket.listen()
        connection , chatPeerAddress = serverSocket.accept()
        chatPeers.append(chatPeerAddress)
        print("Connected; ready to chat!")
        sender = threading.Thread(target=sendThread, args=(connection,))
        receiver = threading.Thread(target=receiveThread, args = (connection,))
        sender.start()
        receiver.start()

def setupChatClient(connection):
    print("Connected; ready to chat!")
    global keepConnection
    keepConnection = True
    chatPeers.append(connection.getpeername())
    sender = threading.Thread(target=sendThread,args=(connection,))
    receiver = threading.Thread(target=receiveThread,args=(connection,))
    sender.start()
    receiver.start()

def sendThread(connection):
    global keepConnection
    while keepConnection:
        if not tobesentMessages.empty():
            message = tobesentMessages.get()
            connection.send(message.encode('UTF-8'))
            if message == "end":
                keepConnection = False
                index = chatPeers.index(connection.getpeername())
                chatPeers.remove(connection.getpeername())
                broadcastPeers.pop(index)
                print("Connection closed")
        time.sleep(0.5)
    connection.close()

def receiveThread(connection):
    global keepConnection
    while keepConnection:
        message = connection.recv(1024)
        message = message.decode('UTF-8').split()
        if message[0] == 'end':
            index = chatPeers.index(connection.getpeername())
            chatPeers.remove(connection.getpeername())
            broadcastPeers.pop(index)
            connection.send("got your end".encode('UTF-8'))
            keepConnection = False
            print("Connection closed")
        elif message[0] == '$':
            print(' '.join(message[1:len(message)]))
    connection.close()
