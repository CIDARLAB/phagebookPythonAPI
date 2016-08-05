"""from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
from twisted.internet import defer
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


    def _new_request_id(self):
        self.requestId += 1
        return self.requestId


    def queue(self, channel, data, options=None):
        s = socket.socket()
        s.setblocking(False)

        try:
            s.connect((self.serverURL,self.port))
        except ConnectionError:
            print("Socket connection refused")
            return Q_Deferred()
        except BlockingIOError:
            # This will always occur simply because blocking is disabled,
            # Socket connections always require code blocking.
            pass
        except:
            print("queue: Unidentified exception while trying to use socket")
            return Q_Deferred()

        requestId = self._new_request_id()
        message = {
            "channel": channel,
            "requestId": requestId,
            "data": data
        }
        if options is not None:
            message["options"] = options
        message = json.dumps(message)  # stringified JSON

        # Pause on socket communication. Instead, queue socket in selector.
        callback = lambda: self._on_open(s, message)
        self.selector.register(s.fileno(), EVENT_WRITE, callback)
        self.pendingRequests += 1

        deferred = Q_Deferred()  # Create user callback register
        self.callBackHash[channel + str(requestId)] = deferred.callback

        return deferred  # Google/Youtube it if you don't know what deferred is


    def resolve_queue(self):
        while self.pendingRequests is not 0:
            events = self.selector.select()
            for key, mask in events:
                event_handler = key.data
                event_handler()


    def _on_open(self, s, outgoing_message):
        print("Connection opened")
        self.selector.unregister(s.fileno())

        s.send(outgoing_message.encode())  # byte string message

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

        chunk = s.recv()
        if chunk:   # still have something to receive
            buffer.append(chunk)
            callback = lambda: self._on_message(s, buffer)
            self.selector.register(s.fileno(), EVENT_READ, callback)
        else:
            # done receiving. parse the message
            print("Done receiving")
            receivedString = b''.join(buffer).decode()

            try:
                mappedData = json.loads(receivedString)
                if self._no_data_is_missing_in(mappedData):
                    callback = self.callBackHash[mappedData["channel"] + str(mappedData["requestId"])]
                    callback(mappedData["data"])  # Undefined callbacks simply won't be executed
            except:
                print("_on_message: Unable to map received data to dictionary (%s)" % receivedString)

            self.pendingRequests -= 1"""

import websocket
import threading
import time

def on_message(ws, message):
    print("Received " + message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(10):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    threading._start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://echo.websocket.org/",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close,
                                on_open=on_open)
    ws.run_forever()