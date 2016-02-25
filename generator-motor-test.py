import matplotlib.pyplot as plt
import matplotlib.animation as animation
import ClassLibrary.motor_tests as mt
from ClassLibrary.client_tool_watcher import client_tool_watcher
from LeapControllers.leap import Controller
from ClassLibrary.handleXML import XMLhandler
import atexit


#  Create the connection to the leap controller
listener = client_tool_watcher()
listener.buildForUI()  # Initiate the leap listener for use with the graphing software
controller = Controller()
controller.add_listener(listener)


#  Create the XMLhandler object needed to record the data
XMLBuilder = XMLhandler('maze_ui_data')
XMLBuilder.createXMLfile()
atexit.register(XMLBuilder.exit_handler)


class Scope:

    # Create the initial test
    def __init__(self, ax, listener):

        self.simplelinetest = mt.SimpleLineTest(ax, listener)

    def update(self, list):

        return self.simplelinetest.update(list)


def emitter():

    while True:
        listener.xPos = listener.xPos + 250
        listener.yPos = listener.yPos + 50
        listener._COUNTER = listener._COUNTER + 1
        listener.frame = str(listener._COUNTER).zfill(10)
        XMLBuilder.append2XML(listener)
        list = [listener.xPos, listener.yPos]
        yield list

fig, ax = plt.subplots(figsize=(10,10))
ax.axis([0, 500, 500, 0])

scope = Scope(ax, listener)

ani = animation.FuncAnimation(fig, scope.update, emitter, interval=10, blit=False)

plt.show()
