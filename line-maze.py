import matplotlib.pyplot as plt
import matplotlib.animation as animation
from ClassLibrary.client_tool_watcher import client_tool_watcher
from ClassLibrary.handleXML import XMLhandler
from LeapControllers.leap import Controller
import atexit

# Create the XMLhandler object needed to record the data
XMLBuilder = XMLhandler('maze_ui_data')
XMLBuilder.createXMLfile()
atexit.register(XMLBuilder.exit_handler)

listener = client_tool_watcher()
listener.buildForUI()
controller = Controller()
controller.add_listener(listener)

class scope():

    def __init__(self, ax):

        self.xData = [0]
        self.yData = [0]
        self.ax = ax
        self.ax.axis([0, 500, 0, 500])
        self.ax.plot([50, 450], [275, 275], linewidth=3.0, color='b')
        self.ax.plot([50, 450], [225, 225], linewidth=3.0, color='b')
        self.ax.plot([50, 450], [250, 250], '--', linewidth=1.0, color='b')
        self.point = self.ax.plot(self.xData,self.yData, 'ro', markersize=10)

    def update(self,list):

        self.ax.lines.remove(ax.lines[3])
        self.xData[0]=list[0]
        self.yData[0]=list[1]
        if listener._COUNTER < 400:
            listener.color = 'R'
            self.ax.plot(self.xData, self.yData, 'ro', markersize=10)
        elif 400 <= listener._COUNTER < 800:
            listener.color = 'Y'
            self.ax.plot(self.xData, self.yData, 'yo', markersize=10)
        elif 800 <= listener._COUNTER < 1200:
            listener.color = 'G'
            self.ax.plot(self.xData, self.yData, 'go', markersize=10)
        elif listener._COUNTER >= 1200:
            quit()

        return self.ax.plot

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
ax.axis([0, 500, 500 ,0])

Scope = scope(ax)

ani = animation.FuncAnimation(fig, Scope.update, emitter, interval=10, blit=False)

plt.show()
