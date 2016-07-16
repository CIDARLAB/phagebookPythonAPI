from random import random
import phagebookAPI

phagebook = phagebookAPI.Phagebook("cidarlab.org",9090)
tempProjectID = 0
tempOrderID = 0

phagebook.create_status("joonhohan365@gmail.com","12345","Weehee PB API Works! ID: %f" % random())
phagebook.get_projects("joonhohan365@gmail.com","12345")
phagebook.get_project("joonhohan365@gmail.com","12345",tempProjectID)
phagebook.create_project_status("joonhohan365@gmail.com","12345",tempProjectID,"Project status # %f" % random())
phagebook.get_orders("joonhohan365@gmail.com","12345")
phagebook.get_order("joonhohan365@gmail.com","12345",tempOrderID)
phagebook.change_ordering_status("joonhohan365@gmail.com","12345",tempOrderID,"Order status # %f" % random())

