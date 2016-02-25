import xml.etree.ElementTree as ET
from xml.dom import minidom


class XMLhandler():

    def __init__(self, filename):

        self.docName = str(filename)

    def createXMLfile(self):

        self.root = ET.Element('Test')
        self.tree = ET.ElementTree(self.root)

    def append2XML(self, object):

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
        self.root.append(self.dataPoint)

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
        output_file = open('tmp/XML_' + self.docName + '.xhtml', 'w')
        output_file.write(reparsed.toprettyxml(indent= "    "))
        output_file.close()