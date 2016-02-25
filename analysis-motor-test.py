import xml.etree.ElementTree
import matplotlib.pyplot as plt
import numpy as np

# Choos the XML data file to process
e = xml.etree.ElementTree.parse('tmp/XML_maze_ui_data.xhtml').getroot()
#e = xml.etree.ElementTree.parse('tmp/XML_Server_Tx.xhtml').getroot()

# The valid data bracket to eliminate spurious data elements that occur in the y direction
bracket = 30

# Create colour coded lists that correspond to the speed levels in of the test
listOfReds = [[], [], [], [], []]  # Slow
listOfYellows = [[], [], [], [], []]  # Medium
listOfGreens = [[], [], [], [], []]  # Fast


# Add the data to ColourList that was selected in the list statement
def appendcolourlist(colourlist):

    colourlist[0].append(float(xPosition))
    colourlist[1].append(float(yPosition))
    colourlist[2].append(np.absolute(float(xVelocity)))  # Get the modulus of the Velocity
    colourlist[3].append(np.absolute(float(yVelocity)))  # Get the modulus of the Velocity
    colourlist[4].append(yDiff)

# Unpack all of the XML data
for child in e:
    frame = int(child.attrib['key'])
    xPosition = child.find('xPos').text
    yPosition = child.find('yPos').text
    xVelocity = child.find('xVel').text
    yVelocity = child.find('yVel').text
    color = child.find('Colour').text

    yDiff = ((250 - float(yPosition)) ** 2)  # For each data point, get the vertical difference from the line to follow

    # Sort the data according to the colour code of the data point
    if yDiff < bracket:

        if color == 'R':
            colourList = listOfReds
            appendcolourlist(colourList)
        elif color == 'Y':
            colourList = listOfYellows
            appendcolourlist(colourList)
        elif color == 'G':
            colourList = listOfGreens
            appendcolourlist(colourList)


# Create the figures and plots the data
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(30, 10))

ax1.axis([0, 500, 0, 500])
ax1.set_xlabel('X Displacement')
ax1.set_ylabel('Y Displacement')
ax1.plot(listOfReds[0], listOfReds[1], 'r.')
ax1.plot(listOfYellows[0], listOfYellows[1], 'y.')
ax1.plot(listOfGreens[0], listOfGreens[1], 'g.')

ax2.axis([0, 2000, 0, 300])
ax2.set_xlabel('X Velocity (mm/s)')
ax2.set_ylabel('Y Velocity (mm/s)')
ax2.plot(listOfReds[2], listOfReds[3], 'r.')
ax2.plot(listOfYellows[2], listOfYellows[3], 'y.')
ax2.plot(listOfGreens[2], listOfGreens[3], 'g.')

ax3.axis([0, 2000, 0, bracket + 10])
ax3.set_xlabel('X Velocity (mm/s)')
ax3.set_ylabel('Y Displacement From Indicated Line')
ax3.plot(listOfReds[2], listOfReds[4], 'r.')
ax3.plot(listOfYellows[2], listOfYellows[4], 'y.')
ax3.plot(listOfGreens[2], listOfGreens[4], 'g.')

ax4.axis([0, 500, 0, bracket + 10])
ax4.set_xlabel('Y Velocity (mm/s)')
ax4.set_ylabel('Y Displacement From Indicated Line')
ax4.plot(listOfReds[3], listOfReds[4], 'r.')
ax4.plot(listOfYellows[3], listOfYellows[4], 'y.')
ax4.plot(listOfGreens[3], listOfGreens[4], 'g.')

plt.show()
