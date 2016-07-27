from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
from twisted.internet import defer
from logging import error, debug
import socket
import json
# Import twisted API for deferred object (download with pip by doing [sudo pip3 install twisted]).
# If you do not know what twisted or asynchronous programming is, look it up.

class Q_Deferred:
    def __init__(self):
        self.d = defer.Deferred()

    def then(self, callback):
        return self.d.addCallback(callback)

    def on_error(self, errback):
        return self.d.addErrback(errback)

    def callback(self, result=None):
        self.d.callback(result)

class Client:
    def __init__(self, serverURL, port=80):
        self.serverURL = serverURL
        self.port = port
        self.selector = DefaultSelector()
        self.pendingRequests = 0
        self.requestId = -1  # A number that will be associated with each socket channel request (ask Prashant
                        # about this concept)
        self.callBackHash = {}  # We are using async programming. This is where we store the callbacks
                           # to process the retrieved info
        # self.messageCache = []
        # '''Asynchronous programming is usually single-threaded so the WebSocket will not send
        #     info until it opens connection or is ready to send. In the off chance the user writes a script that
        #     sends info before socket is ready, handle this by storing those calls here (if any are made) and
        #     executing them in 'connectionMade'.'''

    def _new_request_id(self):
        self.requestId += 1
        return self.requestId

    # People can call "addCallBack(functionName)" to the returned deferred to
    # process received data later from the server.
    # The 'functionName' is a function that handles received data. Data type depends on protocol.
    def queue(self, channel, data, options=None):
        s = socket.socket()
        s.setblocking(False)
        try:
            s.connect((self.serverURL,self.port))
        except BlockingIOError:
            # This will always occur simply because blocking is disabled,
            # despite socket connections always requiring blocking (waiting for connection).
            pass
        except:
            print("queue: Unidentified exception while trying to use socket")
            return Q_Deferred()

        # Formatting data that's to be sent.
        requestId = self._new_request_id()
        message = {
            "channel": channel,
            "requestId": requestId,
            "data": data
        }
        if options is not None:
            message["options"] = options
        message = json.dumps(message)  # stringified JSON

        # Pause with socket protocol. Instead, queue it in selector.
        callback = lambda: self._on_open(s, message)
        self.selector.register(s.fileno(), EVENT_WRITE, callback)
        self.pendingRequests += 1

        deferred = Q_Deferred()  # Create user callback register
        self.callBackHash[channel + str(requestId)] = deferred.callback

        return deferred  # Google/Youtube it if you don't know what deferred is

    def resolve_queue(self):
        while self.pendingRequests is not None:
            events = self.selector.select()
            for key, mask in events:
                event_handler = key.data
                event_handler()

    def _on_open(self, s, outgoing_message):
        print("Connection opened")
        self.selector.unregister(s.fileno())

        s.send(outgoing_message.encode())  # byte string message

        # now register to listen for a message
        receive_buffer = []
        callback = lambda: self._on_message(s, receive_buffer)
        self.selector.register(s.fileno(), EVENT_READ, callback)

    def _no_data_is_missing_in(self,mappedData):
        received_item_checklist = {
            "channel"  :mappedData.get("channel"),
            "requestId":mappedData.get("requestId"),
            "data"     :mappedData.get("data")
        }
        for category in list(received_item_checklist.keys()):
            if received_item_checklist[category] is None:  # a.k.a. missing
                print("_no_data_is_missing_in: data from server does not contain %s", category)
                return False
        return True

    def _on_message(self, s, buffer):
        print("Message received")
        self.selector.unregister(s.fileno())
        chunk = s.recv(1000)
        if chunk:   # still have something to receive
            buffer.append(chunk)
            callback = lambda: self._on_message(s, buffer)
            self.selector.register(s.fileno(), EVENT_READ, callback)
        else:
            # done receiving. parse the message
            print("Done receiving")
            try:
                mappedData = json.loads((b''.join(buffer)).decode())
                if self._no_data_is_missing_in(mappedData):
                    callback = self.callBackHash[mappedData["channel"] + str(mappedData["requestId"])]
                    callback(mappedData["data"])  # Undefined callbacks simply won't be executed
            except:
                print("_on_message: Unable to map received data to dictionary")
            self.pendingRequests -= 1

#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
#         Helper Functions to handle deferred objects       #
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
# def _send_when_ready(client, channel, data, options):
#     return client.emit(channel, data, options)
#
# def _add_callback(deferred, callback):
#     return deferred.addCallBack(callback)
#
# def _add_errback(deferred, errback):
#     return deferred.addErrBack(errback)

#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
#      Master Object that creates connection to server      #
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
# class ServerConnection:
#     def __init__(self, serverURL, port=80):
#         self.serverURL = serverURL
#         self.port = port
#
#     def emit(self, channel, data, options=None):
#         if type(data) is not dict:
#             self.incoming_connection = defer.Deferred()
#             error("CidarAPI interface: data emitted must be dictionary")
#             return self
#         cidar_client = TCP4ClientEndpoint(reactor, self.serverURL, self.port)
#         self.incoming_connection = cidar_client.connect(CidarFactory())
#         self.incoming_connection.addCallback(_send_when_ready, channel, data, options)
#         return self
#
#     def then(self, callback):
#         self.incoming_connection.addCallback(_add_callback,callback)
#         return self
#
#     def handle_error_with(self, errback):
#         self.incoming_connection.addCallback(_add_errback,errback)
#         return self
