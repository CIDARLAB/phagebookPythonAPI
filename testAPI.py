from random import random
import phagebookAPI
import time

phagebook = phagebookAPI.Phagebook("localhost",9090)
tempProjectID = 0
tempOrderID = 0

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

username = "1234@qwer.com"
password = 1234

print("!!!!!!!! Start protocol !!!!!!!!!\n")
start = time.time()

phagebook.create_status(username,password,"Weehee PB API Works! ID: %f" % random()).then(print)

phagebook.get_projects(username,password).then(save_proj_id)
phagebook.get_project(username,password,tempProjectID).then(print)
phagebook.create_project_status(username,password,tempProjectID,"Project status # %f" % random()).then(print)

phagebook.get_orders(username,password).then(save_order_id)
phagebook.get_order(username,password,tempOrderID).then(print)
phagebook.change_ordering_status(username, password, tempOrderID, phagebook.APPROVED).then(print)

phagebook.resolve_queue()

print('took %.2f seconds' % (time.time() - start))