from twisted.internet import reactor, protocol, defer
import socket
import json
# Import twisted API for asynchronous networking (download with pip by doing [sudo pip3 install twisted]).
# If you do not know what twisted or asynchronous programming is, look it up.

# Socket implementation is in this class.
# Protocol implementation is in Phagebook class.
class PhagebookClient(protocol.Protocol):

    def __init__(self, serverURL, port=80):
        self.callBackHash = {}  # We are using async programming. This is where we store the callbacks
                                # to process the retrieved info
        self.messageCache = []
        '''Asynchronous programming is usually single-threaded so the WebSocket will not send
            info until it opens connection or is ready to send. In the off chance the user writes a script that
            sends info before socket is ready, handle this by storing those calls here (if any are made) and
            executing them in this socket.onopen() method.'''
        self.requestId = -1  # A number that will be associated with each socket channel request (ask Prashant
                             # about this concept)

        #reactor.run()

    def makeConnection(self, transport):
        Server = socket.socket()
        Server.connect(())

    def connectionMade(self):
        for messages in self.messageCache:
            self.transport.write(messages)
        self.transport.loseConnection()

    def dataReceived(self, data):
        mappedData = json.loads(data)
        deferred = self.callBackHash[mappedData["channel"] + mappedData["requestId"]]
        deferred.callback(mappedData["data"])

    def _new_request_id(self):
        self.requestId += 1
        return self.requestId

    def _create_message(self, channel, requestId, userEmail, password, objectId, status):
        data = {"username": userEmail, "password": password}
        if objectId is not None:
            data["id"] = objectId
        if status is not None:
            data["status"] = status

        message = {"channel": channel, "requestId": requestId, "data": data}
        return json.dumps(message)

    def emit(self, channel, userEmail, password, objectId=None, status=None):
        requestId = self._new_request_id()
        message = self._create_message(channel, requestId, userEmail, password, objectId, status)

        deferred = defer.Deferred()  # item that handles async abstraction
        self.callBackHash[channel + requestId] = deferred

        return deferred