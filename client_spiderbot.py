from twisted.internet import reactor, protocol
from ClassLibrary.client_tool_watcher import Client_Tool_Watcher
import LeapControllers.leap as leap
import atexit
from ClassLibrary.xml_builder import Accuracy_Test_Builder
import time

listener = Client_Tool_Watcher()
controller = leap.Controller()
controller.add_listener(listener)

print 'Starting...'


class ClientProtocol(protocol.Protocol):

    def __init__(self, factory):

        self.factory = factory

        # Comment Out Under Normal Operation. For Accuracy Tracker Only.
        #listener.build_video()
        #listener.buildForUI()
        #self.file_bulder = Accuracy_Test_Builder("Accuaracy_Test")
        #self.file_bulder.createXMLfile()
        #atexit.register(self.file_bulder.exit_handler)

    def connectionMade(self):
        self.sendData()

    def sendData(self):

        self.transport.write(data)
        #  time.sleep(0.04) ## Uncomment when using home machine as host

    def SendModData(self):

        self.transport.write(listener.compString)

        # Comment Out Under Normal Operation. For Accuracy Tracker Only.
        #indX, indY = listener.run_video()
        #self.file_bulder.append_user_movement_data_to_xml(listener)
        #self.file_bulder.save_accuracy_parameters("{0:.0f}".format(indX), "{0:.0f}".format(indY))
        #print "Video Information:"
        #print "Indicated x Position: {0:.0f}".format(indX)
        #print "Indicated y Position: {0:.0f}".format(indY)

    def dataReceived(self, data):
        print "Server Response:\n", data
        #  time.sleep(0.004) ## Uncomment when using home machine as host
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

    reactor.connectTCP('kebaiz.com', 8080, Factory(data))
    #reactor.connectTCP('<Insert Home Machine Name>', 8000, Factory(data))

    reactor.run()
