import xml.etree.ElementTree as ET
from xml.dom import minidom


class Operation_XML_Builder():

    def __init__(self, filename):

        self.docName = str(filename)

    def createXMLfile(self):

        self.root = ET.Element('Test')
        self.tree = ET.ElementTree(self.root)

        self.tests = ET.Element("TestFrames")
        self.root.append(self.tests)

    def append_user_movement_data_to_xml(self, object):

        frame = object.frame
        xPos = object.xPos
        yPos = object.yPos
        zPos = object.zPos
        xVel = object.xVel
        yVel = object.yVel
        zVel = object.zVel
        xPxL = object.xPressureLeft
        xPxR = object.xPressureRight
        yPxU = object.yPressureUp
        yPxD = object.yPressureDown
        color = object.color

        self.dataPoint = ET.Element("Frame")
        self.dataPoint.set('key', str(frame))
        self.tests.append(self.dataPoint)

        self.xPosElement = ET.Element("xPos")
        self.xPosElement.text = str(xPos)
        self.dataPoint.append(self.xPosElement)

        self.yPosElement = ET.Element("yPos")
        self.yPosElement.text = str(yPos)
        self.dataPoint.append(self.yPosElement)

        self.zPosElement = ET.Element("zPos")
        self.zPosElement.text = str(zPos)
        self.dataPoint.append(self.zPosElement)

        self.xVelElement = ET.Element("xVel")
        self.xVelElement.text = str(xVel)
        self.dataPoint.append(self.xVelElement)

        self.yVelElement = ET.Element("yVel")
        self.yVelElement.text = str(yVel)
        self.dataPoint.append(self.yVelElement)

        self.zVelElement = ET.Element("zVel")
        self.zVelElement.text = str(zVel)
        self.dataPoint.append(self.zVelElement)

        self.xPxLElement = ET.Element("XPxLeft")
        self.xPxLElement.text = str(xPxL)
        self.dataPoint.append(self.xPxLElement)

        self.xPxRElement = ET.Element("XPxRight")
        self.xPxRElement.text = str(xPxR)
        self.dataPoint.append(self.xPxRElement)

        self.yPxUElement = ET.Element("YPxUp")
        self.yPxUElement.text = str(yPxU)
        self.dataPoint.append(self.yPxUElement)

        self.yPxDElement = ET.Element("YPxDown")
        self.yPxDElement.text = str(yPxD)
        self.dataPoint.append(self.yPxDElement)

        self.color = ET.Element("Colour")
        self.color.text = str(color)
        self.dataPoint.append(self.color)



    def exit_handler(self):

        print "Saving Data..."

        #self.tree.write('tmp/PLAIN_' + self.docName)

        rough_string = ET.tostring(self.root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        output_file = open('tmp/' + self.docName + '.xhtml', 'w')
        output_file.write(reparsed.toprettyxml(indent= "    "))
        output_file.close()

        print "Data Saved. Exiting."


class Test_XML_Builder(Operation_XML_Builder):

    def save_test_parameters_to_xml(self, test_object):

        testee = test_object.test_instance.name
        conditions = test_object.test_instance.conditions
        profession = test_object.test_instance.profession
        testtype = test_object.test_instance.tests(test_object.test_instance.testtype)
        axisheight = test_object.axis_height
        axiswidth = test_object.axis_width
        testlength = test_object.test_length
        boundary = test_object.boundary

        self.testeeinfo = ET.Element("TestSubjectInformation")
        self.testeeinfo.text = str("")
        self.root.append(self.testeeinfo)

        self.testee = ET.Element("Testee")
        self.testee.text = str(testee)
        self.testeeinfo.append(self.testee)

        self.conditions = ET.Element("Conditions")
        self.conditions.text = str(conditions)
        self.testeeinfo.append(self.conditions)

        self.profession = ET.Element("Profession")
        self.profession.text = str(profession)
        self.testeeinfo.append(self.profession)

        self.testinfo = ET.Element("TestInformation")
        self.testinfo.text = str("")
        self.root.append(self.testinfo)

        self.testtype = ET.Element("Test")
        self.testtype.text = str(testtype)
        self.testinfo.append(self.testtype)

        self.axis_height = ET.Element("AxisHeight")
        self.axis_height.text = str(axisheight)
        self.testinfo.append(self.axis_height)

        self.axis_width = ET.Element("AxisWidth")
        self.axis_width.text = str(axiswidth)
        self.testinfo.append(self.axis_width)

        self.test_length = ET.Element("TestLength")
        self.test_length.text = str(testlength)
        self.testinfo.append(self.test_length)

        self.boundary = ET.Element("Boundary")
        self.boundary.text = str(boundary)
        self.testinfo.append(self.boundary)

    def append_transient_test_details(self, test_object):

        testtype = test_object.test_instance.testtype

        if str(testtype) == "2":

            self.transient = ET.Element("TransientTestData")
            self.transient.text = str("")
            self.dataPoint.append(self.transient)

            self.xSpot = ET.Element("XPosCurrentSpot")
            self.xSpot.text = str(test_object.rand_x + 100)
            self.transient.append(self.xSpot)

            self.ySpot = ET.Element("YPosCurrentSpot")
            self.ySpot.text = str (test_object.rand_y + 100)
            self.transient.append(self.ySpot)
