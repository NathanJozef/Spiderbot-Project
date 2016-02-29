from ClassLibrary.xml_builder import Test_XML_Builder
import atexit
import numpy as np

#  Super Class that implements only one methods, the BuildTestXML method.
#  This ensures test files are annoted correctly with the test details
class TestBuilder:

    def __init__(self):
        pass

    def build_test_xml(self, test_instance):

        #  Create the file name for the test
        XMLFileName = test_instance.create_test_filename()

        #  Create the XMLhandler object needed to record the data
        self.XMLBuilder = Test_XML_Builder(XMLFileName)
        self.XMLBuilder.createXMLfile()
        atexit.register(self.XMLBuilder.exit_handler)

        self.xRange = 500
        self.yRange = 300
        self.zRange = 300


class Single_Line_Test(TestBuilder):

    def __init__(self, ax, listener, test_instance):

        #  Set the variables for the test frmae
        self.axis_height = 500
        self.axis_width = 500
        self.test_instance = test_instance
        self.build_test_xml(self.test_instance)
        self.listener = listener
        self.xData = [0]
        self.yData = [0]
        self.test_length = 600
        self.boundary = 10
        self.ax = ax

        #  Build the test frame
        self.ax.axis([0, self.axis_width, 0, self.axis_height])
        self.ax.plot([50, 450], [250 + self.boundary, 250 + self.boundary], linewidth=3.0, color='b')
        self.ax.plot([50, 450], [250 - self.boundary, 250 - self.boundary], linewidth=3.0, color='b')
        self.ax.plot([50, 450], [250, 250], '--', linewidth=1.0, color='b')
        self.point = self.ax.plot(self.xData, self.yData, 'ro', markersize=10)

        self.XMLBuilder.save_test_parameters_to_xml(self)

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

        self.XMLBuilder.append_user_movement_data_to_xml(self.listener)

        return self


class Diagonal_Line_Test(TestBuilder):

    def __init__(self, ax, listener, test_instance):

        #  Set the variables for the test frmae
        self.axis_height = 500
        self.axis_width = 500
        self.test_instance = test_instance
        self.build_test_xml(self.test_instance)
        self.listener = listener
        self.xData = [0]
        self.yData = [0]
        self.test_length = 600
        self.boundary = 20
        self.ax = ax

        #  Build the test frame
        self.ax.axis([0, self.axis_width, 0, self.axis_height])
        self.ax.plot([50, 450], [50 + self.boundary, 450 + self.boundary], linewidth=3.0, color='b')
        self.ax.plot([50, 450], [50 - self.boundary, 450 - self.boundary], linewidth=3.0, color='b')
        self.ax.plot([50, 450], [50, 450], '--', linewidth=1.0, color='b')
        self.point = self.ax.plot(self.xData, self.yData, 'ro', markersize=10)

        self.XMLBuilder.save_test_parameters_to_xml(self)

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

        self.XMLBuilder.append_user_movement_data_to_xml(self.listener)

        return self


class Move_To_Dots_Test(TestBuilder):

    def __init__(self, ax, listener, test_instance):

        #  Set the variables for the test frmae
        self.axis_height = 500
        self.axis_width = 500
        self.test_instance = test_instance
        self.build_test_xml(self.test_instance)
        self.listener = listener
        self.xData = [0]
        self.yData = [0]
        self.test_length = 1000
        self.boundary = 40
        self.ax = ax
        self.rand_x = np.random.random_integers(0, self.axis_height * 0.6)
        self.rand_y = np.random.random_integers(0, self.axis_height * 0.6)

        #  Build the test frame
        self.ax.axis([0, self.axis_width, 0, self.axis_height])
        self.ax.plot([self.rand_x + 100, self.rand_x + 100], [self.rand_y + 100, self.rand_y + 100], 'bo',
                     markersize=30)
        self.point = self.ax.plot(self.xData, self.yData, 'ro', markersize=self.boundary)

        self.XMLBuilder.save_test_parameters_to_xml(self)

    def update(self, list):

        self.ax.lines.remove(self.ax.lines[1])
        self.xData[0] = self.listener.xPos
        self.yData[0] = self.listener.yPos
        if self.listener.COUNTER % 100 == 0:
            self.ax.lines.remove(self.ax.lines[0])
            self.rand_x = np.random.random_integers(0, self.axis_width * 0.6)
            self.rand_y = np.random.random_integers(0, self.axis_height * 0.6)
            self.ax.plot([self.rand_x + 100, self.rand_x + 100], [self.rand_y + 100, self.rand_y + 100], 'bo',
                         markersize=self.boundary)
        self.ax.plot(self.xData, self.yData, 'ro', markersize=10)
        #  Set the colour of the indicator to inform the user of the speed to generate
        if self.listener.COUNTER >= self.test_length:
            quit()

        self.XMLBuilder.append_user_movement_data_to_xml(self.listener)

        return self
