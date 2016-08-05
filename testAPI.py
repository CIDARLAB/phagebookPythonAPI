from random import random
import phagebookAPI
import time

phagebook = phagebookAPI.Phagebook("ws://localhost:9090/websocket/")
username = "1234@qwer.com"
password = 1234

def callboth(data):
    global username
    global password
    print("Received Projects: " + str(data))
    phagebook.get_project(username,password,data[0]["projectId"]).then(print)
    phagebook.create_project_status(username,password,data[0]["projectId"],"Project status # %f" % random()).then(print)

def callall(data):
    global username
    global password
    print("Received Orders: " + str(data))
    phagebook.get_order(username,password,data[0]["orderId"]).then(print)
    phagebook.change_ordering_status(username, password, data[0]["orderId"], phagebook.APPROVED).then(print)

print("!!!!!!!! Start protocol !!!!!!!!!\n")
start = time.time()

phagebook.create_status(username,password,"Weehee PB API Works! ID: %f" % random()).then(print)
phagebook.get_projects(username,password).then(callboth)
phagebook.get_orders(username,password).then(callall)

while phagebook.phagebookClient.socket.pendingRequests:
    pass

print('took %.2f seconds' % (time.time() - start))