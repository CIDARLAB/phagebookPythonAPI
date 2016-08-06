from twisted.internet import defer
import websocket
import threading
import json

class Q_Deferred:
    def __init__(self):
        self.d = defer.Deferred()

    def then(self, callback):
        return self.d.addCallback(callback)

    def on_error(self, errback):
        return self.d.addErrback(errback)

    def callback(self, result=None):
        self.d.callback(result)

class ClientWebSocket:
    def __init__(self, serverURL):
        self.requestId = -1  # A number that will be associated with each socket channel request (ask Prashant
                        # about this concept)
        def _on_message(ws, message):
            print("Message received")
            try:
                mappedData = json.loads(message)
                received_item_checklist = {
                    "channel"  :mappedData.get("channel"),
                    "requestId":mappedData.get("requestId"),
                    "data"     :mappedData.get("data")
                }
                for category in list(received_item_checklist.keys()):
                    if received_item_checklist[category] is None:  # a.k.a. data missing
                        print("ERROR _no_data_is_missing_in: data from server does not contain %s", category)
                        return

                callback = ws.callBackHash[mappedData["channel"] + str(mappedData["requestId"])]
                callback(mappedData["data"])  # Undefined callbacks simply won't be executed
            except:
                print("ERROR _on_messssage: Unable to map received data to dictionary (%s)" % message)

            ws.pendingRequests -= 1
            if ws.pendingRequests is 0:
                ws.close()

        def _on_error(ws, error):
            print("_on_error:" + str(error))

        def _on_close(ws):
            print("### closed ###")

        def _on_open(ws):
            print("Connection opened")
            ws.attempting = False
            for each_message in ws.messageCache:
                ws.send(each_message.encode())
            ws.messageCache.clear()

        self.socket = websocket.WebSocketApp(serverURL,
                                on_message=_on_message,
                                on_error=_on_error,
                                on_close=_on_close,
                                on_open=_on_open)
        self.socket.attempting = False
        self.socket.pendingRequests = 0
        self.socket.callBackHash = {}  
        # ^ We are using async programming. This is where we store the callbacks
        # to process the retrieved info
        self.socket.messageCache = [] 
        # ^ Socket communications will be run on a separate thread
        # Since the socket may take time to open, we will cache the messages here so that
        # it sends the messages when the socket opens. This allows to do someting else while waiting for the socket to open.


    def _send_when_ready(self, message):
        self.socket.pendingRequests += 1
        try:
            self.socket.send(message.encode())
        except websocket.WebSocketException as e: # Socket isn't open. open it. Attempt to open it only once
            print("Caching message: " + message)
            if not self.socket.attempting:
                threading._start_new_thread(self.socket.run_forever, ())
                self.socket.attempting = True
            self.socket.messageCache.append(message)


    def _new_request_id(self):
        self.requestId += 1
        return self.requestId


    def emit(self, channel, data, options=None):
        requestId = self._new_request_id()
        message = {
            "channel": channel,
            "requestId": requestId,
            "data": data
        }
        if options is not None:
            message["options"] = options
        message = json.dumps(message)

        deferred = Q_Deferred()
        self.socket.callBackHash[channel + str(requestId)] = deferred.callback
        self._send_when_ready(message)  # send here so users have time to add callback on deferred
        return deferred  # Google/Youtube it if you don't know what deferred is