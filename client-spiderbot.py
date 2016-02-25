from twisted.internet import reactor, protocol
from ClassLibrary.client_tool_watcher import client_tool_watcher
import atexit, time
import LeapControllers.leap as leap

listener = client_tool_watcher()
controller = leap.Controller()
controller.add_listener(listener)

print 'Starting...'

class ClientProtocol(protocol.Protocol):

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.sendData()

    def sendData(self):
        self.transport.write(data)
        #time.sleep(0.04) ## Uncomment when using home machine as host

    def SendModData(self):
        self.transport.write(listener.compString)

    def dataReceived(self, data):
        print "Server Response:\n", data
        #time.sleep(0.004) ## Uncomment when using home machine as host
        self.SendModData()

class Factory(protocol.ClientFactory):

    def __init__(self, data):
        self.data = data

    def buildProtocol(self, addr):
        return ClientProtocol(self)

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed."
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print "Connection lost."
        #reactor.stop()

def exit_handler():
    print "Exiting..."
    controller.remove_listener(listener)

atexit.register(exit_handler)

if __name__ == "__main__":
    data = "cli_0000000_0000000_0000000_0000000_0000000_0000000"

    reactor.connectTCP('54.194.135.20', 8000, Factory(data))
    #reactor.connectTCP('<Insert Home Machine Name>', 8000, Factory(data))

    reactor.run()
