from ClassLibrary.xml_builder import Test_XML_Builder
import atexit
import numpy as np
from collections import deque

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

        self.leadIn = 100
        self.test_length = 2000
        self.boundary = 20
        self.axis_height = 400
        self.axis_width = 400
        self.xData = self.axis_width / 2
        self.yData = self.axis_height / 2
        self.leaderDirection = 1.0


class Horizontal_Line_Test(TestBuilder):

    def __init__(self, ax, listener, test_instance):

        #  Set the variables for the test frmae
        self.test_instance = test_instance
        self.build_test_xml(self.test_instance)
        self.listener = listener
        self.ax = ax
        self.leaderXPos = 50

        #  Build the test frame
        self.ax.axis([0, self.axis_width, 0, self.axis_height])
        self.ax.plot([50, 350], [(self.axis_height / 2) + self.boundary, (self.axis_width / 2) + self.boundary],
                     linewidth=3.0, color='b')
        self.ax.plot([50, 350], [(self.axis_width / 2) - self.boundary, (self.axis_width / 2) - self.boundary],
                     linewidth=3.0, color='b')
        self.ax.plot([50, 350], [(self.axis_width / 2), (self.axis_height / 2)], '--', linewidth=1.0, color='b')
        self.point = self.ax.plot(self.xData, self.yData, 'ro', markersize=10)
        self.leader = self.ax.plot(self.leaderXPos, self.axis_height / 2, 'bo', markersize=20)

        self.XMLBuilder.save_test_parameters_to_xml(self)

    def update(self, list):

        self.ax.lines.remove(self.ax.lines[4])
        self.ax.lines.remove(self.ax.lines[3])
        self.xData = self.listener.xPos
        self.yData = self.listener.yPos

        #  Set the colour of the indicator to inform the user of the speed to generate
        if self.listener.COUNTER - self.leadIn < 0:

            self.ax.plot(self.leaderXPos, self.axis_height / 2, 'bo', markersize=20)

            self.listener.color = 'B'
            self.ax.plot(self.xData, self.yData, 'bo', markersize=10)

        elif 0 <= self.listener.COUNTER - self.leadIn < self.test_length/3:

            self.leaderXPos += (1 * self.leaderDirection)
            self.ax.plot(self.leaderXPos, self.axis_height / 2, 'bo', markersize=20)

            self.listener.color = 'R'

            new_Y_data = ((self.yData - self.axis_height / 2) / self.test_instance.linear_coefficients[0]) + (self.axis_height / 2)
            difference = self.yData - new_Y_data
            print 'the difference is:', difference
            self.yData = new_Y_data
            self.listener.yPos = self.yData

            self.ax.plot(self.xData, self.yData, 'ro', markersize=10)

        elif self.test_length / 3 <= self.listener.COUNTER - self.leadIn < 2 * self.test_length/3:

            self.leaderXPos += (2.5 * self.leaderDirection)
            self.ax.plot(self.leaderXPos, self.axis_height / 2, 'bo', markersize=20)

            self.listener.color = 'Y'

            new_Y_data = ((self.yData - self.axis_height / 2) / self.test_instance.linear_coefficients[1]) + (self.axis_height / 2)
            difference = self.yData - new_Y_data
            print 'the difference is:', difference
            self.yData = new_Y_data
            self.listener.yPos = self.yData

            self.ax.plot(self.xData, self.yData, 'yo', markersize=10)

        elif 2 * self.test_length/3 <= self.listener.COUNTER - self.leadIn < self.test_length:

            self.leaderXPos += (5 * self.leaderDirection)
            self.ax.plot(self.leaderXPos, self.axis_height / 2, 'bo', markersize=20)

            self.listener.color = 'G'

            new_Y_data = ((self.yData - self.axis_height / 2) / self.test_instance.linear_coefficients[2]) + (self.axis_height / 2)
            difference = self.yData - new_Y_data
            print 'the difference is:', difference
            self.yData = new_Y_data
            self.listener.yPos = self.yData

            self.ax.plot(self.xData, self.yData, 'go', markersize=10)

        elif self.listener.COUNTER - self.leadIn >= self.test_length:

            quit()

        if self.leaderXPos > 350:
            self.leaderDirection = -1.0
        elif self.leaderXPos < 50:
            self.leaderDirection = 1.0

        self.XMLBuilder.append_user_movement_data_to_xml(self.listener)

        return self

class Vertical_Line_Test(TestBuilder):

    def __init__(self, ax, listener, test_instance):

        #  Set the variables for the test frmae
        self.test_instance = test_instance
        self.build_test_xml(self.test_instance)
        self.listener = listener
        self.ax = ax
        self.leaderYPos = 50

        #  Build the test frame
        self.ax.axis([0, self.axis_width, 0, self.axis_height])
        self.ax.plot([(self.axis_width / 2) + self.boundary, (self.axis_width / 2) + self.boundary], [50, 350],
                     linewidth=3.0, color='b')
        self.ax.plot([(self.axis_width / 2) - self.boundary, (self.axis_width / 2) - self.boundary], [50, 350],
                     linewidth=3.0, color='b')
        self.ax.plot([(self.axis_width / 2), (self.axis_height / 2)], [50, 350], '--', linewidth=1.0, color='b')
        self.point = self.ax.plot(self.xData, self.yData, 'ro', markersize=10)
        self.leader = self.ax.plot(self.axis_width / 2, self.leaderYPos, 'bo', markersize=20)

        self.XMLBuilder.save_test_parameters_to_xml(self)

    def update(self, list):

        self.ax.lines.remove(self.ax.lines[4])
        self.ax.lines.remove(self.ax.lines[3])
        self.xData = self.listener.xPos
        self.yData = self.listener.yPos

        #  Set the colour of the indicator to inform the user of the speed to generate
        if self.listener.COUNTER - self.leadIn < 0:

            self.ax.plot(self.axis_width / 2, self.leaderYPos, 'bo', markersize=20)

            self.listener.color = 'B'
            self.ax.plot(self.xData, self.yData, 'bo', markersize=10)

        elif 0 <= self.listener.COUNTER - self.leadIn < self.test_length/3:

            self.leaderYPos += (1 * self.leaderDirection)
            self.ax.plot(self.axis_width / 2, self.leaderYPos, 'bo', markersize=20)

            self.listener.color = 'R'

            new_X_data = ((self.xData - self.axis_width / 2) / self.test_instance.vertical_coefficients[0]) + (self.axis_width / 2)
            difference = self.xData - new_X_data
            print 'the difference is:', difference
            self.xData = new_X_data
            self.listener.xPos = self.xData

            self.ax.plot(self.xData, self.yData, 'ro', markersize=10)

        elif self.test_length / 3 <= self.listener.COUNTER - self.leadIn < 2 * self.test_length/3:

            self.leaderYPos += (2.5 * self.leaderDirection)
            self.ax.plot(self.axis_width / 2, self.leaderYPos, 'bo', markersize=20)

            self.listener.color = 'Y'

            new_X_data = ((self.xData - self.axis_width / 2) / self.test_instance.vertical_coefficients[1]) + (self.axis_width / 2)
            difference = self.xData - new_X_data
            print 'the difference is:', difference
            self.xData = new_X_data
            self.listener.xPos = self.xData

            self.ax.plot(self.xData, self.yData, 'yo', markersize=10)

        elif 2 * self.test_length/3 <= self.listener.COUNTER - self.leadIn < self.test_length:

            self.leaderYPos += (5 * self.leaderDirection)
            self.ax.plot(self.axis_width / 2, self.leaderYPos, 'bo', markersize=20)

            self.listener.color = 'G'

            new_X_data = ((self.xData - self.axis_width / 2) / self.test_instance.vertical_coefficients[2]) + (self.axis_width / 2)
            difference = self.xData - new_X_data
            print 'the difference is:', difference
            self.xData = new_X_data
            self.listener.xPos = self.xData

            self.ax.plot(self.xData, self.yData, 'go', markersize=10)

        elif self.listener.COUNTER - self.leadIn >= self.test_length:

            quit()

        if self.leaderYPos > 350:
            self.leaderDirection = -1.0
        elif self.leaderYPos < 50:
            self.leaderDirection = 1.0

        self.XMLBuilder.append_user_movement_data_to_xml(self.listener)

        return self


class Diagonal_Line_Validation(TestBuilder):

    def __init__(self, ax, listener, test_instance):

        #  Set the variables for the test frmae
        self.test_instance = test_instance
        self.build_test_xml(self.test_instance)
        self.listener = listener
        self.ax = ax
        self.leaderXPos = 100
        self.minPoint = 100
        self.maxPoint = 300

        #  Build the test frame
        self.ax.axis([0, self.axis_width, 0, self.axis_height])
        self.ax.plot([self.minPoint, self.maxPoint], [self.minPoint + self.boundary, self.maxPoint + self.boundary], linewidth=3.0, color='b')
        self.ax.plot([self.minPoint, self.maxPoint], [self.minPoint - self.boundary, self.maxPoint - self.boundary], linewidth=3.0, color='b')
        self.ax.plot([self.minPoint, self.maxPoint], [self.minPoint, self.maxPoint], '--', linewidth=1.0, color='b')
        self.point = self.ax.plot(self.xData, self.yData, 'ro', markersize=10)
        self.leader = self.ax.plot(self.leaderXPos, self.leaderXPos, 'bo', markersize=20)

        self.XMLBuilder.save_test_parameters_to_xml(self)


    def update(self, list):

        self.ax.lines.remove(self.ax.lines[4])
        self.ax.lines.remove(self.ax.lines[3])
        self.xData = self.listener.xPos
        self.yData = self.listener.yPos

        #  Set the colour of the indicator to inform the user of the speed to generate
        if self.listener.COUNTER - self.leadIn < 0:

            self.ax.plot(self.leaderXPos, self.leaderXPos, 'bo', markersize=20)

            self.listener.color = 'B'
            self.ax.plot(self.xData, self.yData, 'bo', markersize=10)

        if 0 <= self.listener.COUNTER - self.leadIn < self.test_length/3:

            self.leaderXPos += (1 * self.leaderDirection)
            self.ax.plot(self.leaderXPos, self.leaderXPos, 'bo', markersize=20)

            self.listener.color = 'R'

            new_X_data = ((self.xData - self.leaderXPos) / self.test_instance.vertical_coefficients[0]) + (self.leaderXPos)
            difference = self.xData - new_X_data
            print 'the X difference  is:', difference
            self.xData = new_X_data
            new_Y_data = ((self.yData - self.leaderXPos) / self.test_instance.linear_coefficients[0]) + (self.leaderXPos)
            difference = self.yData - new_Y_data
            print 'the Y difference is:', difference
            self.yData = new_Y_data

            self.listener.yPos = self.yData
            self.listener.xPos = self.xData

            self.ax.plot(self.xData, self.yData, 'ro', markersize=10)

        elif self.test_length/3 <= self.listener.COUNTER - self.leadIn < 2*self.test_length/3:

            self.leaderXPos += (2.5 * self.leaderDirection)
            self.ax.plot(self.leaderXPos, self.leaderXPos, 'bo', markersize=20)

            self.listener.color = 'Y'

            new_X_data = ((self.xData - self.leaderXPos) / self.test_instance.vertical_coefficients[1]) + (self.leaderXPos)
            difference = self.xData - new_X_data
            print 'the X difference  is:', difference
            self.xData = new_X_data
            new_Y_data = ((self.yData - self.leaderXPos) / self.test_instance.linear_coefficients[1]) + (self.leaderXPos)
            difference = self.yData - new_Y_data
            print 'the Y difference is:', difference
            self.yData = new_Y_data

            self.listener.yPos = self.yData
            self.listener.xPos = self.xData

            self.ax.plot(self.xData, self.yData, 'yo', markersize=10)

        elif 2*self.test_length/3 <= self.listener.COUNTER - self.leadIn < self.test_length:

            self.leaderXPos += (5 * self.leaderDirection)
            self.ax.plot(self.leaderXPos, self.leaderXPos, 'bo', markersize=20)

            self.listener.color = 'G'

            new_X_data = ((self.xData - self.leaderXPos) / self.test_instance.vertical_coefficients[1]) + (self.leaderXPos)
            difference = self.xData - new_X_data
            print 'the X difference  is:', difference
            self.xData = new_X_data
            new_Y_data = ((self.yData - self.leaderXPos) / self.test_instance.linear_coefficients[1]) + (self.leaderXPos)
            difference = self.yData - new_Y_data
            print 'the Y difference is:', difference
            self.yData = new_Y_data

            self.listener.yPos = self.yData
            self.listener.xPos = self.xData

            self.ax.plot(self.xData, self.yData, 'go', markersize=10)

        elif self.listener.COUNTER >= self.test_length:
            quit()

        if self.leaderXPos > self.maxPoint:
            self.leaderDirection = -1.0
        elif self.leaderXPos < self.minPoint:
            self.leaderDirection = 1.0

        self.XMLBuilder.append_user_movement_data_to_xml(self.listener)

        return self


class Accuracy_Test(TestBuilder):

    def __init__(self, ax, listener, test_instance):

        #  Set the variables for the test frmae
        self.test_instance = test_instance
        self.build_test_xml(self.test_instance)
        self.listener = listener
        self.ax = ax
        self.rand_x = np.random.random_integers(0, self.axis_height * 0.5)
        self.rand_y = np.random.random_integers(0, self.axis_height * 0.5)
        self.xVelQueue = [0, 0, 0, 0, 0]
        self.yVelQueue = [0, 0, 0, 0, 0]
        self.averageXVels = 0
        self.averageYVels = 0

        #  Build the test frame
        self.ax.axis([0, self.axis_width, 0, self.axis_height])
        self.ax.plot([self.rand_x + 100, self.rand_x + 100], [self.rand_y + 100, self.rand_y + 100], 'bs',
                     markersize=self.boundary)
        self.point = self.ax.plot(self.xData, self.yData, 'ro', markersize=10)

        self.XMLBuilder.save_test_parameters_to_xml(self)

    def update(self, list):

        self.oldXData = self.xData
        self.oldYData = self.yData

        self.ax.lines.remove(self.ax.lines[1])
        self.xData = self.listener.xPos
        self.yData = self.listener.yPos

        self.xVelQueue.pop(0)
        self.xVelQueue.append(float('{0:.2f}'.format(np.absolute(self.listener.xVel))))
        self.yVelQueue.pop(0)
        self.yVelQueue.append(float('{0:.2f}'.format(np.absolute(self.listener.yVel))))
        self.averageXVels = sum(self.xVelQueue) / len(self.xVelQueue)
        self.averageYVels = sum(self.yVelQueue) / len(self.yVelQueue)

        if self.averageXVels < self.test_instance.accuracy_coefficients[0] and \
            self.averageYVels < self.test_instance.accuracy_coefficients[1]:

            print 'X Pos Modified:', self.xData - self.oldXData
            print 'Y Pos Modified:', self.yData - self.oldYData

            self.xData = self.oldXData
            self.yData = self.oldYData


        if self.listener.COUNTER % 100 == 0:
            self.ax.lines.remove(self.ax.lines[0])
            self.rand_x = np.random.random_integers(0, self.axis_width * 0.5)
            self.rand_y = np.random.random_integers(0, self.axis_height * 0.5)
            self.ax.plot([self.rand_x + 100, self.rand_x + 100], [self.rand_y + 100, self.rand_y + 100], 'bs',
                         markersize=self.boundary)

        if self.listener.COUNTER - self.leadIn < 0:

            self.listener.color = 'B'
            self.ax.plot(self.xData, self.yData, 'bo', markersize=10)

        elif self.listener.COUNTER - self.leadIn >= 0:

            if self.xData - (self.rand_x + 100) < (self.boundary / 2) \
                    and (self.rand_x + 100) - self.xData < (self.boundary / 2) \
                    and self.yData - (self.rand_y + 100) < (self.boundary / 2) \
                    and (self.rand_y + 100) - self.yData < (self.boundary / 2):

                self.listener.color = 'Y'
                self.ax.plot(self.xData, self.yData, 'yo', markersize=10)

            else:

                self.listener.color = 'R'
                self.ax.plot (self.xData, self.yData, 'ro', markersize=10)

        #  Set the colour of the indicator to inform the user of the speed to generate
        if self.listener.COUNTER >= self.test_length:
            quit()

        self.XMLBuilder.append_user_movement_data_to_xml(self.listener)
        self.XMLBuilder.append_transient_test_details(self)

        return self
