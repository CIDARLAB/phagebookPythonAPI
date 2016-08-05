from random import random
import phagebookAPI
import time

phagebook = phagebookAPI.Phagebook("ws://localhost:9090/websocket/")
# phagebook = phagebookAPI.Phagebook("ws://echo.websocket.org/")
tempProjectID = 0
tempOrderID = 0

# def save_proj_id(data):
#     global tempProjectID
#     tempProjectID= data[0]["projectId"]
#     print("ALL PROJECTS !!!!!!!!!")
#     for project in data:
#         print(project)
#
# def save_order_id(data):
#     global tempOrderID
#     tempOrderID= data[0]["orderId"]
#     print("KACHING! ORDERS !!!!!!!!!")
#     for order in data:
#         print(order)

def callboth(data):
    username = "1234@qwer.com"
    password = 1234
    phagebook.get_project(username,password,data[0]["projectId"]).then(print)
    phagebook.create_project_status(username,password,data[0]["projectId"],"Project status # %f" % random()).then(print)

def callall(data):
    username = "1234@qwer.com"
    password = 1234
    phagebook.get_order(username,password,data[0]["orderId"]).then(print)
    phagebook.change_ordering_status(username, password, data[0]["orderId"], phagebook.APPROVED).then(print)

username = "1234@qwer.com"
password = 1234

print("!!!!!!!! Start protocol !!!!!!!!!\n")
start = time.time()

phagebook.create_status(username,password,"Weehee PB API Works! ID: %f" % random()).then(print)
phagebook.get_projects(username,password).then(callboth)
phagebook.get_orders(username,password).then(callall)
#
# phagebook.resolve_queue()
while phagebook.phagebookClient.socket.pendingRequests:
    pass

print('took %.2f seconds' % (time.time() - start))