import threading
import UDPBroadcaster
import chatModule

stopBListen = threading.Event()
stopBroadcast = threading.Event()
chatPeerFound = threading.Event()



while True:
    command = input()
    if command == "broadcast":
        stopBroadcast.clear()
        t = threading.Thread(target = UDPBroadcaster.broadcast, args = (stopBroadcast,))
        t.start()
    elif command == "broadcast listen":
        stopBListen.clear()
        t = threading.Thread(target = UDPBroadcaster.broadcastListen , args = (stopBListen,))
        t.start()
    elif command == "stop broadcast":
        stopBroadcast.set()
    elif command == "stop broadcast listen":
        stopBListen.set()
    elif len(command) > 0 and command[0] == '$':
        chatModule.tobesentMessages.put(command)
    elif command == "end":
        chatModule.tobesentMessages.put(command)



