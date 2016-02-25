from ClassLibrary.handleXML import XMLhandler
import atexit

#  Create the XMLhandler object needed to record the data
XMLBuilder = XMLhandler('maze_ui_data')
XMLBuilder.createXMLfile()
atexit.register(XMLBuilder.exit_handler)

class SimpleLineTest:

    def __init__(self, ax, listener):

        self.listener = listener
        self.xData = [0]
        self.yData = [0]
        self.ax = ax
        self.ax.axis([0, 500, 0, 500])
        self.ax.plot([50, 450], [275, 275], linewidth=3.0, color='b')
        self.ax.plot([50, 450], [225, 225], linewidth=3.0, color='b')
        self.ax.plot([50, 450], [250, 250], '--', linewidth=1.0, color='b')
        self.point = self.ax.plot(self.xData, self.yData, 'ro', markersize=10)

    def update(self, list):

        self.listener.xPos += 250
        self.listener.yPos += 50

        self.ax.lines.remove(self.ax.lines[3])
        self.xData[0] = self.listener.xPos
        self.yData[0] = self.listener.yPos

        #  Set the colour of the indicator to inform the user of the speed to generate
        if self.listener.COUNTER < 400:
            self.listener.color = 'R'
            self.ax.plot(self.xData, self.yData, 'ro', markersize=10)
        elif 400 <= self.listener.COUNTER < 800:
            self.listener.color = 'Y'
            self.ax.plot(self.xData, self.yData, 'yo', markersize=10)
        elif 800 <= self.listener.COUNTER < 1200:
            self.listener.color = 'G'
            self.ax.plot(self.xData, self.yData, 'go', markersize=10)
        elif self.listener.COUNTER >= 1200:
            quit()

        XMLBuilder.append2XML(self.listener)

        return self


class DiagonalLineTest:

    def __init__(self, ax, listener):

        self.listener = listener
        self.xData = [0]
        self.yData = [0]
        self.ax = ax
        self.ax.axis([0, 500, 0, 500])
        self.ax.plot([75, 425], [125, 425], linewidth=3.0, color='b')
        self.ax.plot([75, 425], [75, 375], linewidth=3.0, color='b')
        self.ax.plot([75, 425], [100, 400], '--', linewidth=1.0, color='b')
        self.point = self.ax.plot(self.xData, self.yData, 'ro', markersize=10)

    def update(self, list):

        self.listener.xPos += 250
        self.listener.yPos += 50

        self.ax.lines.remove(self.ax.lines[3])
        self.xData[0] = self.listener.xPos
        self.yData[0] = self.listener.yPos

        #  Set the colour of the indicator to inform the user of the speed to generate
        if self.listener.COUNTER < 400:
            self.listener.color = 'R'
            self.ax.plot(self.xData, self.yData, 'ro', markersize=10)
        elif 400 <= self.listener.COUNTER < 800:
            self.listener.color = 'Y'
            self.ax.plot(self.xData, self.yData, 'yo', markersize=10)
        elif 800 <= self.listener.COUNTER < 1200:
            self.listener.color = 'G'
            self.ax.plot(self.xData, self.yData, 'go', markersize=10)
        elif self.listener.COUNTER >= 1200:
            quit()

        XMLBuilder.append2XML(self.listener)

        return self