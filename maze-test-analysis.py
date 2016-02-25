import xml.etree.ElementTree
import matplotlib.pyplot as plt
import numpy as np

# Choos the XML data file to process
#e = xml.etree.ElementTree.parse('tmp/XML_maze_ui_data.xhtml').getroot()
e = xml.etree.ElementTree.parse('tmp/XML_Server_Tx.xhtml').getroot()

# The valid data bracket to eliminate spurious data elements that occur in the y direction
bracket = 30

# Create colour coded lists that correspond to the speed levels in of the test
listofReds = [[], [], [], [], []] # Slow
listofYellows = [[], [], [], [], []] # Medium
listofGreens = [[], [], [], [], []] # Fast

# Add the data to ColourList that was selected in the list statement
def appendColourList(colourList):

    colourList[0].append(float(xPosition))
    colourList[1].append(float(yPosition))
    colourList[2].append(np.sqrt(float(xVelocity) ** 2)) # Get the modulus of the Velocity
    colourList[3].append(np.sqrt(float(yVelocity) ** 2)) # Get the modulus of the Velocity
    colourList[4].append(yDiff)

# Unpack all of the XML data
for child in e:
    frame = int(child.attrib['key'])
    xPosition = child.find('xPos').text
    yPosition = child.find('yPos').text
    xVelocity = child.find('xVel').text
    yVelocity = child.find('yVel').text
    color = child.find('Colour').text

    yDiff = ((250 - float(yPosition)) ** 2) # For each data point, get the vertical difference from the line to follow

    # Sort the data according to the colour code of the data point
    if yDiff < bracket:

        if color == 'R':
            colourList = listofReds
            appendColourList(colourList)
        elif color == 'Y':
            colourList = listofYellows
            appendColourList(colourList)
        elif color == 'G':
            colourList = listofGreens
            appendColourList(colourList)


# Create the figures and plots the data
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(30, 10))

ax1.axis([0, 500, 0, 500])
ax1.set_xlabel('X Displacement')
ax1.set_ylabel('Y Displacement')
ax1.plot(listofReds[0], listofReds[1], 'r.')
ax1.plot(listofYellows[0], listofYellows[1], 'y.')
ax1.plot(listofGreens[0], listofGreens[1], 'g.')

ax2.axis([0, 2000, 0, 300])
ax2.set_xlabel('X Velocity (mm/s)')
ax2.set_ylabel('Y Velocity (mm/s)')
ax2.plot(listofReds[2], listofReds[3], 'r.')
ax2.plot(listofYellows[2], listofYellows[3], 'y.')
ax2.plot(listofGreens[2], listofGreens[3], 'g.')

ax3.axis([0, 2000, 0, bracket + 10])
ax3.set_xlabel('X Velocity (mm/s)')
ax3.set_ylabel('Y Displacement From Indicated Line')
ax3.plot(listofReds[2], listofReds[4], 'r.')
ax3.plot(listofYellows[2], listofYellows[4], 'y.')
ax3.plot(listofGreens[2], listofGreens[4], 'g.')

ax4.axis([0, 500, 0, bracket + 10])
ax4.set_xlabel('Y Velocity (mm/s)')
ax4.set_ylabel('Y Displacement From Indicated Line')
ax4.plot(listofReds[3], listofReds[4], 'r.')
ax4.plot(listofYellows[3], listofYellows[4], 'y.')
ax4.plot(listofGreens[3], listofGreens[4], 'g.')

plt.show()
