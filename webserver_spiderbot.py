from twisted.internet import protocol, reactor
from ClassLibrary.xml_builder import Operation_XML_Builder
from ClassLibrary.server_data_handler import server_data_handler
import pickle, atexit

print ""
print "Connected to Server..."
print ""
print "Set Test Flag"
print ""

test = 'Y'

XMLFrame = Operation_XML_Builder('Server_Tx')
XMLFrame.createXMLfile()

atexit.register(XMLFrame.exit_handler)


class Echo(protocol.Protocol):

    def __init__(self):
        pass

    def combine_data(self):

        combined_object = server_data_handler()

        try:
            leap_object = pickle.load(open("tmp/leap_data_pickle", 'rb'))
            combined_object.xPos = leap_object.xPos
            combined_object.yPos = leap_object.yPos
            combined_object.zPos = leap_object.zPos
            combined_object.xVel = leap_object.xVel
            combined_object.yVel = leap_object.yVel
            combined_object.zVel = leap_object.zVel

        except:
            print "There is no Leap Pickle Object"

        try:
            LabView_object = pickle.load(open("tmp/LabView_data_pickle"))
            combined_object.xPressureLeft = LabView_object.xPressureLeft
            combined_object.xPressureRight = LabView_object.xPressureRight
            combined_object.yPressureUp = LabView_object.yPressureUp
            combined_object.yPressureDown = LabView_object.yPressureDown

        except:
            print "There is no LabView Pickle Object"

        return combined_object



    def dataReceived(self, data):

        # This is only a technical test script.
        # Raw positional data is transmitted only persists in
        # a Technical Test File until the next Technical Test.
        if test == "Y":

            current_frame = server_data_handler()  # Create instance object for the current frame

            if str(data)[:4] == 'cli_':  # Receiving data from the remote Leap computer

                current_frame.append_leapdata(data)
                current_frame.pickle_data_for_LabView()  # Save the current data to the temporary pickle file

            if str(data)[:4] == 'lab_':  # Sending data to the remote LabView Computer

                current_frame.append_pressures(data)
                labview_pos_string = current_frame.unpickle_data_for_Labview()

            current_frame = self.combine_data()
            current_frame.frame = int(current_frame.frame) / 2
            current_frame.frame = str(current_frame.frame).zfill(10)

            print current_frame.__str__() # Print the current data to the Server Terminal
            XMLFrame.append_user_movement_data_to_xml(current_frame)

            if str(data)[:4] == 'cli_':
                self.transport.write(current_frame.__str__())  # Send the current data to the client for confirmation
            elif str(data)[:4] == 'lab_':
                self.transport.write(labview_pos_string)


class EchoFactory(protocol.Factory):

    def buildProtocol(self, addr):
        return Echo()

print "Awaiting Connection..."

reactor.listenTCP(8080, EchoFactory())

reactor.run()



