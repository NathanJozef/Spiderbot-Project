from ClassLibrary.handleXML import XMLhandler
import atexit

#  Super Class that implements only one methods, the BuildTestXML method.
#  This ensures test files are annoted correctly with the test details
class TestBuilder:

    def __init__(self):
        pass

    def BuildTestXML(self, test_instance):

        #  Create the file name for the test
        XMLFileName = test_instance.create_test_filename()

        #  Create the XMLhandler object needed to record the data
        self.XMLBuilder = XMLhandler(XMLFileName)
        self.XMLBuilder.createXMLfile()
        atexit.register(self.XMLBuilder.exit_handler)

        self.xRange = 500
        self.yRange = 300
        self.zRange = 300


class SimpleLineTest(TestBuilder):

    def __init__(self, ax, listener, test_instance):

        #  Set the variables for the test frmae
        self.axis_height = 500
        self.axis_width = 500
        self.maze_left = 0.1 * self.axis_width
        self.maze_right = self.axis_width - (0.1 * self.axis_width)
        self.maze_centre = self.axis_height / 2
        self.maze_upper_bound = self.maze_centre + (0.05 * self.axis_height)
        self.maze_lower_bound = self.maze_centre - (0.05 * self.axis_height)
        self.BuildTestXML(test_instance)
        self.listener = listener
        self.xData = [0]
        self.yData = [0]
        self.test_length = 600
        self.ax = ax

        #  Build the test frame
        self.ax.axis([0, self.axis_width, 0, self.axis_height])
        self.ax.plot([self.maze_left, self.maze_right], [self.maze_upper_bound, self.maze_upper_bound],
                     linewidth=3.0, color='b')
        self.ax.plot([self.maze_left, self.maze_right], [self.maze_lower_bound, self.maze_lower_bound],
                     linewidth=3.0, color='b')
        self.ax.plot([self.maze_left, self.maze_right], [self.maze_centre, self.maze_centre], '--',
                     linewidth=1.0, color='b')
        self.point = self.ax.plot(self.xData, self.yData, 'ro', markersize=10)

    def update(self, list):

        self.ax.lines.remove(self.ax.lines[3])
        self.xData[0] = self.listener.xPos
        self.yData[0] = self.listener.yPos

        #  Set the colour of the indicator to inform the user of the speed to generate
        if self.listener.COUNTER < self.test_length/3:
            self.listener.color = 'R'
            self.ax.plot(self.xData, self.yData, 'ro', markersize=10)
        elif self.test_length/3 <= self.listener.COUNTER < 2*self.test_length/3:
            self.listener.color = 'Y'
            self.ax.plot(self.xData, self.yData, 'yo', markersize=10)
        elif 2*self.test_length/3 <= self.listener.COUNTER < self.test_length:
            self.listener.color = 'G'
            self.ax.plot(self.xData, self.yData, 'go', markersize=10)
        elif self.listener.COUNTER >= self.test_length:
            quit()

        self.XMLBuilder.append2XML(self.listener)

        return self


class DiagonalLineTest(TestBuilder):

    def __init__(self, ax, listener, test_instance):

        self.axis_height = 500
        self.axis_width = 500
        self.maze_left = 0.1 * self.axis_width
        self.maze_right = self.axis_width - (0.1 * self.axis_width)
        self.maze_centre = self.axis_height / 2
        self.maze_upper_bound = self.maze_centre + (0.05 * self.axis_height)
        self.maze_lower_bound = self.maze_centre - (0.05 * self.axis_height)

        self.BuildTestXML(test_instance)
        self.listener = listener
        self.xData = [0]
        self.yData = [0]
        self.ax = ax
        self.ax.axis([0, self.axis_width, 0, self.axis_height])
        self.ax.plot([self.maze_left, self.maze_right], [self.maze_upper_bound, self.maze_upper_bound],
                     linewidth=3.0, color='b')
        self.ax.plot([self.maze_left, self.maze_right], [self.maze_lower_bound, self.maze_lower_bound],
                     linewidth=3.0, color='b')
        self.ax.plot([self.maze_left, self.maze_right], [self.maze_centre, self.maze_centre], '--',
                     linewidth=1.0, color='b')
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

        self.XMLBuilder.append2XML(self.listener)

        return self
