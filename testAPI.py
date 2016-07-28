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

print("!!!!!!!! Start protocol !!!!!!!!!\n")

start = time.time()
phagebook.create_status("joonhohan365@gmail.com","12345","Weehee PB API Works! ID: %f" % random()).then(print)
phagebook.get_projects("joonhohan365@gmail.com","12345").then(save_proj_id)
phagebook.get_project("joonhohan365@gmail.com","12345",tempProjectID).then(print)
phagebook.create_project_status("joonhohan365@gmail.com","12345",tempProjectID,"Project status # %f" % random()).then(print)
phagebook.get_orders("joonhohan365@gmail.com","12345").then(save_order_id)
phagebook.get_order("joonhohan365@gmail.com","12345",tempOrderID).then(print)
phagebook.change_ordering_status("joonhohan365@gmail.com","12345",tempOrderID,"Order status # %f" % random()).then(print)

phagebook.resolve_queue()

print('took %.2f seconds' % (time.time() - start))