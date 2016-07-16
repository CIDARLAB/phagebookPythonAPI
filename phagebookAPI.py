import phagebookClient

# Socket implementation is in ClientSocket class.
# Protocol implementation is in this class.

############### YOU CANNOT HAVE MULTIPLE PHAGEBOOK INSTANCES IN ONE PROGRAM ##############
class Phagebook:

    def __init__(self, phagebookURL, port=80):
        self.clientSocket = phagebookClient.PhagebookClient(phagebookURL, port)

    def create_status(self, userEmail, password, status):
        return self.clientSocket.emit("CREATE_STATUS", userEmail, password,  None, status)

    def get_projects(self, userEmail, password):
        return self.clientSocket.emit("GET_PROJECTS", userEmail, password)

    def get_project(self, userEmail, password, projectID):
        return self.clientSocket.emit("GET_PROJECT", userEmail, password, projectID)

    def create_project_status(self, userEmail, password, projectID, projectStatus):
        return self.clientSocket.emit("CREATE_PROJECT_STATUS", userEmail, password, projectID, projectStatus)

    def get_orders(self, userEmail, password):
        return self.clientSocket.emit("GET_ORDERS", userEmail, password)

    def get_order(self, userEmail, password, orderID):
        return self.clientSocket.emit("GET_ORDER", userEmail, password, orderID)

    def change_ordering_status(self, userEmail, password, orderID, orderStatus):
        return self.clientSocket.emit("CHANGE_ORDERING_STATUS", userEmail, password, orderID, orderStatus)