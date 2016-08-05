import json
import socket
import time

requestId = -1;

def _new_request_id():
    global requestId
    requestId += 1
    return requestId

def _no_data_is_missing_in(mappedData):

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

def get(channel, data, options=None):

    requestId = _new_request_id()
    message = {
        "channel": channel,
        "requestId": requestId,
        "data": data
    }
    if options is not None:
        message["options"] = options
    message = json.dumps(message)  # stringified JSON

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 9090))
    print("Connection opened")
    s.send(message.encode())  # byte string message
    print("Sent message!")

    buf = []
    while True:
        chunk = s.recv(1000)
        if not chunk:
            break
        buf.append(chunk)

    s.close()
    print("Done receiving")
    receivedString = b''.join(buf).decode()

    try:
        mappedData = json.loads(receivedString)
        if _no_data_is_missing_in(mappedData):
            print(mappedData["data"])
    except:
        print("_on_message: Unable to map received data to dictionary (%s)" % receivedString)

username = "1234@qwer.com"
password = 1234

class Phagebook:
    def __init__(self):

        # Order status types
        self.INPROGRESS = "INPROGRESS"
        self.APPROVED = "APPROVED"
        self.SUBMITTED = "SUBMITTED"
        self.DENIED = "DENIED"
        self.RECEIVED = "RECEIVED"

    def _format_data(self, userEmail, password, objectId=None, status=None):
        data = {
            "username": userEmail,
            "password": password
        }
        if objectId is not None:
            data["id"] = objectId
        if status is not None:
            data["status"] = status
        return data

    def create_status(self, userEmail, password, status):
        get("CREATE_STATUS", self._format_data(userEmail, password,  None, status))

    def get_projects(self, userEmail, password):
        get("GET_PROJECTS", self._format_data(userEmail, password))

    def get_project(self, userEmail, password, projectID):
        get("GET_PROJECT", self._format_data(userEmail, password, projectID))

    def create_project_status(self, userEmail, password, projectID, projectStatus):
        get("CREATE_PROJECT_STATUS", self._format_data(userEmail, password, projectID, projectStatus))

    def get_orders(self, userEmail, password):
        get("GET_ORDERS", self._format_data(userEmail, password))

    def get_order(self, userEmail, password, orderID):
        get("GET_ORDER", self._format_data(userEmail, password, orderID))

    def change_ordering_status(self, userEmail, password, orderID, orderStatus):
        get("CHANGE_ORDERING_STATUS", self._format_data(userEmail, password, orderID, orderStatus))

def save_proj_id(data):
    global tempProjectID
    tempProjectID= data[0]["projectId"]
    print("ALL PROJECTS !!!!!!!!!")
    for project in data:
        print(project)

def save_order_id(data):
    global tempOrderID
    tempOrderID= data[0]["orderId"]
    print("KACHING! ORDERS !!!!!!!!!")
    for order in data:
        print(order)

phagebook = Phagebook()

print("START protocol !!!!!!!!\n")
start = time.time()
# phagebook.create_status(username,password,"Weehee PB API Works! ID: %f" % requestId)
phagebook.get_projects(username,password)
# phagebook.get_project(username,password,tempProjectID)
# phagebook.create_project_status(username,password,tempProjectID,"Project status # %f" % requestId)
# phagebook.get_orders(username,password)
# phagebook.get_order(username,password,tempOrderID)
# phagebook.change_ordering_status(username, password, tempOrderID, phagebook.APPROVED)
print('took %.2f seconds' % (time.time() - start))