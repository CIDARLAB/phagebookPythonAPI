from twisted.internet import reactor, defer
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint

class Greeter(Protocol):  # Client
    def connectionMade(self):
        print("MADE!")

    def sendMessage(self, msg):
        self.transport.write("MESSAGE %s\n" % msg)

class GreeterFactory(Factory):
    def buildProtocol(self, addr):
        return Greeter()

class Printer:
    def sendMessage(self, word):
        print(word)

def gotProtocol(p, word, word2):
    p.sendMessage(word)
    return word2


point = TCP4ClientEndpoint(reactor, "cidarlab.org", 9090)
d = point.connect(GreeterFactory())
d.addCallback(gotProtocol,"Hello")
#
# d1 = defer.Deferred()
# d1.addCallback(gotProtocol,"Hello!","Anything?")
# d1.addCallback(print)
# print(d1.callback(Printer()))