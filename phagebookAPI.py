import CidarAPI

# Socket implementation is in ClientSocket class.
# Protocol implementation is in this class.

############### YOU CANNOT HAVE MULTIPLE PHAGEBOOK INSTANCES IN ONE PROGRAM ##############
class Phagebook:
    def __init__(self, phagebookURL, port=80):
        self.clientSocket = CidarAPI.ServerConnection(phagebookURL, port)

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
        return self.clientSocket.emit("CREATE_STATUS", self._format_data(userEmail, password,  None, status))

    def get_projects(self, userEmail, password):
        return self.clientSocket.emit("GET_PROJECTS", self._format_data(userEmail, password))

    def get_project(self, userEmail, password, projectID):
        return self.clientSocket.emit("GET_PROJECT", self._format_data(userEmail, password, projectID))

    def create_project_status(self, userEmail, password, projectID, projectStatus):
        return self.clientSocket.emit("CREATE_PROJECT_STATUS", self._format_data(userEmail, password, projectID, projectStatus))

    def get_orders(self, userEmail, password):
        return self.clientSocket.emit("GET_ORDERS", self._format_data(userEmail, password))

    def get_order(self, userEmail, password, orderID):
        return self.clientSocket.emit("GET_ORDER", self._format_data(userEmail, password, orderID))

    def change_ordering_status(self, userEmail, password, orderID, orderStatus):
        return self.clientSocket.emit("CHANGE_ORDERING_STATUS", self._format_data(userEmail, password, orderID, orderStatus))