from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import reactor, protocol, defer
from logging import error, debug
import json
# Import twisted API for asynchronous networking (download with pip by doing [sudo pip3 install twisted]).
# If you do not know what twisted or asynchronous programming is, look it up.

#   #   #   #   #   #   #   #   #   #   #   #   #   #
#        Object that handles transmitted data       #
#   #   #   #   #   #   #   #   #   #   #   #   #   #
class CidarClient(protocol.Protocol):
    def __init__(self):
        self.requestId = -1  # A number that will be associated with each socket channel request (ask Prashant
                        # about this concept)
        self.callBackHash = {}  # We are using async programming. This is where we store the callbacks
                           # to process the retrieved info
        self.messageCache = []
        '''Asynchronous programming is usually single-threaded so the WebSocket will not send
            info until it opens connection or is ready to send. In the off chance the user writes a script that
            sends info before socket is ready, handle this by storing those calls here (if any are made) and
            executing them in 'connectionMade'.'''

    def makeConnection(self, transport):
        self.transport = transport

    def connectionMade(self):
        debug("Connection opened")
        for each_message in self.messageCache:
            self.transport.write(each_message)
        self.messageCache.clear()

    def _no_data_is_missing_in(self,mappedData):
        received_item_checklist = {
            "channel"  :mappedData.get("channel"),
            "requestId":mappedData.get("requestId"),
            "data"     :mappedData.get("data")
        }
        for category in list(received_item_checklist.keys()):
            if received_item_checklist[category] is None:  # a.k.a. missing
                error("Server data error: data from server does not contain %s", category)
                return False
        return True

    def dataReceived(self, data):
        mappedData = json.loads(data)
        if self._no_data_is_missing_in(mappedData):
            callback = self.callBackHash[mappedData["channel"] + str(mappedData["requestId"])]
            callback(mappedData["data"])  # Undefined callbacks simply won't be executed

    def _new_request_id(self):
        self.requestId += 1
        return self.requestId

    def emit(self, channel, dictionaryData, options):
        requestId = self._new_request_id()
        message = {
            "channel": channel,
            "requestId": requestId,
            "data": dictionaryData
        }
        if options is not None:
            message["options"] = options
        self.transport.write(json.dumps(message))  # send data

        deferred = defer.Deferred()  # Create async networking handler
        self.callBackHash[channel + str(requestId)] = deferred.callback
        return deferred


#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
#         Object that handles creating "connection instances" = protocols       #
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
class CidarFactory(protocol.Factory):
    protocol = CidarClient

    def doStart(self):
        print("Factory starts")

    def clientConnectionFailed(self, connector, reason):
        debug(reason)

    def clientConnectionLost(self, connector, unused_reason):
        debug(unused_reason)

    def startedConnecting(self, connectorInstance):
        debug(connectorInstance)

    def buildProtocol(self, address):
        return self.protocol(address)

    def doStop(self):
        print("Factory stops")

#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
#         Helper Functions to handle deferred objects       #
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
def _send_when_ready(client, channel, data, options):
    return client.emit(channel, data, options)

def _add_callback(deferred, callback):
    return deferred.addCallBack(callback)

def _add_errback(deferred, errback):
    return deferred.addErrBack(errback)

#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
#      Master Object that creates connection to server      #
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
class ServerConnection:
    def __init__(self, serverURL, port=80):
        self.serverURL = serverURL
        self.port = port

    def emit(self, channel, data, options=None):
        if type(data) is not dict:
            self.incoming_connection = defer.Deferred()
            error("CidarAPI interface: data emitted must be dictionary")
            return self
        cidar_client = TCP4ClientEndpoint(reactor, self.serverURL, self.port)
        self.incoming_connection = cidar_client.connect(CidarFactory())
        self.incoming_connection.addCallback(_send_when_ready, channel, data, options)
        return self

    def then(self, callback):
        self.incoming_connection.addCallback(_add_callback,callback)
        return self

    def handle_error_with(self, errback):
        self.incoming_connection.addCallback(_add_errback,errback)
        return self
