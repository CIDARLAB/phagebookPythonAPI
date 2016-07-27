from random import random
import phagebookAPI
import time

phagebook = phagebookAPI.Phagebook("cidarlab.org",9090)
tempProjectID = 0
tempOrderID = 0

start = time.time()
phagebook.create_status("joonhohan365@gmail.com","12345","Weehee PB API Works! ID: %f" % random()).then(print)
# phagebook.get_projects("joonhohan365@gmail.com","12345").then(print)
# phagebook.get_project("joonhohan365@gmail.com","12345",tempProjectID).then(print)
# phagebook.create_project_status("joonhohan365@gmail.com","12345",tempProjectID,"Project status # %f" % random()).then(print)
# phagebook.get_orders("joonhohan365@gmail.com","12345").then(print)
# phagebook.get_order("joonhohan365@gmail.com","12345",tempOrderID).then(print)
# phagebook.change_ordering_status("joonhohan365@gmail.com","12345",tempOrderID,"Order status # %f" % random()).then(print)

print("!!!!!!!! Start protocol !!!!!!!!!\n")
phagebook.resolve_queue()

print('took %.2f seconds' % (time.time() - start))