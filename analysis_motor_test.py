import xml.etree.ElementTree
import matplotlib.pyplot as plt
import numpy as np
import sys
from ClassLibrary.test_builder import TestBuilder
from scipy.optimize import curve_fit
from scipy.integrate import quad
from ClassLibrary.profiler import Profiler

def horizontal_line_test_analysis():

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

    def func(x, a, c):
        return a * x + c

    def characteristic_equation(x):
        return popt[0] * x + popt[1]

    for child in e[0]:

        frame = int(child.attrib['key'])
        xPosition = child.find('xPos').text
        yPosition = child.find('yPos').text
        xVelocity = child.find('xVel').text
        yVelocity = child.find('yVel').text
        yDiff = np.absolute((float(axis_height) / 2) - float(yPosition))  # For each data point, get the vertical difference from the line to follow
        colour = child.find('Colour').text

        # Sort the data according to the colour code of the data point
        if yDiff < boundary:

            if colour == 'R':
                colourList = listOfReds
                appendcolourlist(colourList)
            elif colour == 'Y':
                colourList = listOfYellows
                appendcolourlist(colourList)
            elif colour == 'G':
                colourList = listOfGreens
                appendcolourlist(colourList)

    # Create the figures and plots the data
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(30, 10))

    ax1.axis([0, int(axis_width), 0, int(axis_width)])
    ax1.set_xlabel('X Displacement')
    ax1.set_ylabel('Y Displacement')
    ax1.plot(listOfReds[0], listOfReds[1], 'ro')
    ax1.plot(listOfYellows[0], listOfYellows[1], 'yo')
    ax1.plot(listOfGreens[0], listOfGreens[1], 'go')

    red_mean_displacement = sum(listOfReds[4]) / len(listOfReds[4])
    yellow_mean_displacement = sum(listOfYellows[4]) / len(listOfYellows[4])
    green_mean_displacement = sum(listOfGreens[4]) / len(listOfGreens[4])
    red_mean_velocity = sum(listOfReds[2]) / len(listOfReds[2])
    yellow_mean_velocity = sum(listOfYellows[2]) / len(listOfYellows[2])
    green_mean_velocity = sum(listOfGreens[2]) / len(listOfGreens[2])

    ax2.axis([0, max(listOfGreens[2]) + (float(max(listOfGreens[2])) * 0.1), 0, max(listOfGreens[4]) + (float(max(listOfGreens[4]) * 0.1))])
    ax2.set_xlabel('X Velocity (mm/s)')
    ax2.set_ylabel('Y Displacement')
    ax2.plot(listOfReds[2], listOfReds[4], 'ro')
    ax2.plot(listOfYellows[2], listOfYellows[4], 'yo')
    ax2.plot(listOfGreens[2], listOfGreens[4], 'go')

    # Plot the lines for the average displacement and the average velocities for each of the movmement profiles
    ax2.plot([0, 2000], [red_mean_displacement, red_mean_displacement], 'r--', linewidth=3)
    ax2.plot([0, 2000], [yellow_mean_displacement, yellow_mean_displacement], 'y--', linewidth=3)
    ax2.plot([0, 2000], [green_mean_displacement, green_mean_displacement], 'g--', linewidth=3)
    ax2.plot([red_mean_velocity, red_mean_velocity], [0, 2000], 'r--', linewidth=3)
    ax2.plot([yellow_mean_velocity, yellow_mean_velocity], [0, 2000], 'y--', linewidth=3)
    ax2.plot([green_mean_velocity, green_mean_velocity], [0, 2000], 'g--', linewidth=3)

    # Plot the exact points of average velocity and average displacement cross over
    ax2.plot([red_mean_velocity, red_mean_velocity], [red_mean_displacement , red_mean_displacement], 'ro', markersize =30)
    ax2.plot([yellow_mean_velocity, yellow_mean_velocity], [yellow_mean_displacement, yellow_mean_displacement], 'yo', markersize=30)
    ax2.plot([green_mean_velocity, green_mean_velocity], [green_mean_displacement, green_mean_displacement], 'go', markersize=30)

    xdata = [red_mean_velocity, yellow_mean_velocity, green_mean_velocity]
    ydata = [red_mean_displacement, yellow_mean_displacement, green_mean_displacement]

    popt, pcov = curve_fit(func, xdata, ydata)

    x = np.linspace(0, max(listOfGreens[2]) + (float(max(listOfGreens[2])) * 0.1), 100)
    y = func(x, popt[0], popt[1])
    ax2.plot(x,y, 'b', linewidth=3.0)

    red_integral = (quad(characteristic_equation, 0, red_mean_velocity))[0]
    yellow_integral = (quad(characteristic_equation, red_mean_velocity, yellow_mean_velocity))[0]
    green_integral = (quad(characteristic_equation, yellow_mean_velocity, green_mean_velocity))[0]

    red_coefficient = red_integral / red_integral
    yellow_coefficient = yellow_integral / red_integral
    green_coefficient = green_integral / red_integral

    return red_coefficient, yellow_coefficient, green_coefficient

def vertical_line_test_analysis():

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
        colourlist[4].append(xDiff)

    def func(x, a, c):
        return a * x + c

    def characteristic_equation(x):
        return popt[0] * x + popt[1]

    for child in e[0]:

        frame = int(child.attrib['key'])
        xPosition = child.find('xPos').text
        yPosition = child.find('yPos').text
        xVelocity = child.find('xVel').text
        yVelocity = child.find('yVel').text
        xDiff = np.absolute((float(axis_width) / 2) - float(xPosition))  # For each data point, get the vertical difference from the line to follow
        colour = child.find('Colour').text

        # Sort the data according to the colour code of the data point
        if xDiff < boundary:

            if colour == 'R':
                colourList = listOfReds
                appendcolourlist(colourList)
            elif colour == 'Y':
                colourList = listOfYellows
                appendcolourlist(colourList)
            elif colour == 'G':
                colourList = listOfGreens
                appendcolourlist(colourList)

    # Create the figures and plots the data
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(30, 10))

    ax1.axis([0, int(axis_width), 0, int(axis_width)])
    ax1.set_xlabel('X Displacement')
    ax1.set_ylabel('Y Displacement')
    ax1.plot(listOfReds[0], listOfReds[1], 'ro')
    ax1.plot(listOfYellows[0], listOfYellows[1], 'yo')
    ax1.plot(listOfGreens[0], listOfGreens[1], 'go')

    red_mean_displacement = sum(listOfReds[4]) / len(listOfReds[4])
    yellow_mean_displacement = sum(listOfYellows[4]) / len(listOfYellows[4])
    green_mean_displacement = sum(listOfGreens[4]) / len(listOfGreens[4])
    red_mean_velocity = sum(listOfReds[3]) / len(listOfReds[3])
    yellow_mean_velocity = sum(listOfYellows[3]) / len(listOfYellows[3])
    green_mean_velocity = sum(listOfGreens[3]) / len(listOfGreens[3])

    ax2.axis([0, max(listOfGreens[3]) + (float(max(listOfGreens[3])) * 0.1), 0, max(listOfGreens[4]) + (float(max(listOfGreens[4]) * 0.1))])
    ax2.set_xlabel('Y Velocity (mm/s)')
    ax2.set_ylabel('X Displacement')
    ax2.plot(listOfReds[3], listOfReds[4], 'ro')
    ax2.plot(listOfYellows[3], listOfYellows[4], 'yo')
    ax2.plot(listOfGreens[3], listOfGreens[4], 'go')

    # Plot the lines for the average displacement and the average velocities for each of the movmement profiles
    ax2.plot([0, 2000], [red_mean_displacement, red_mean_displacement], 'r--', linewidth=3)
    ax2.plot([0, 2000], [yellow_mean_displacement, yellow_mean_displacement], 'y--', linewidth=3)
    ax2.plot([0, 2000], [green_mean_displacement, green_mean_displacement], 'g--', linewidth=3)
    ax2.plot([red_mean_velocity, red_mean_velocity], [0, 2000], 'r--', linewidth=3)
    ax2.plot([yellow_mean_velocity, yellow_mean_velocity], [0, 2000], 'y--', linewidth=3)
    ax2.plot([green_mean_velocity, green_mean_velocity], [0, 2000], 'g--', linewidth=3)

    # Plot the exact points of average velocity and average displacement cross over
    ax2.plot([red_mean_velocity, red_mean_velocity], [red_mean_displacement , red_mean_displacement], 'ro', markersize =30)
    ax2.plot([yellow_mean_velocity, yellow_mean_velocity], [yellow_mean_displacement, yellow_mean_displacement], 'yo', markersize=30)
    ax2.plot([green_mean_velocity, green_mean_velocity], [green_mean_displacement, green_mean_displacement], 'go', markersize=30)

    xdata = [red_mean_velocity, yellow_mean_velocity, green_mean_velocity]
    ydata = [red_mean_displacement, yellow_mean_displacement, green_mean_displacement]

    popt, pcov = curve_fit(func, xdata, ydata)

    x = np.linspace(0, max(listOfGreens[3]) + (float(max(listOfGreens[3])) * 0.1), 100)
    y = func(x, popt[0], popt[1])
    ax2.plot(x,y, 'b', linewidth=3.0)

    red_integral = (quad(characteristic_equation, 0, red_mean_velocity))[0]
    yellow_integral = (quad(characteristic_equation, red_mean_velocity, yellow_mean_velocity))[0]
    green_integral = (quad(characteristic_equation, yellow_mean_velocity, green_mean_velocity))[0]

    red_coefficient = red_integral / red_integral
    yellow_coefficient = yellow_integral / red_integral
    green_coefficient = green_integral / red_integral

    return red_coefficient, yellow_coefficient, green_coefficient

def diagonal_line_test_analysis():

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
        colourlist[4].append(minDistance)

    def func(x, a, c):
        return a * x + c

    def characteristic_equation(x):
        return popt[0] * x + popt[1]

    for child in e[0]:

        frame = int(child.attrib['key'])
        xPosition = child.find('xPos').text
        yPosition = child.find('yPos').text
        xVelocity = child.find('xVel').text
        yVelocity = child.find('yVel').text
        xDiff = np.absolute(float(yPosition) - float(xPosition))  # For each data point, get the horizontal difference from the line to follow
        yDiff = np.absolute(float(xPosition) - float(yPosition))  # For each data point, get the vertical difference from the line to follow
        minDistance = np.sqrt(np.square(yDiff) / 2)
        colour = child.find('Colour').text

        # Sort the data according to the colour code of the data point
        if minDistance < boundary:

            if colour == 'R':
                colourList = listOfReds
                appendcolourlist(colourList)
            elif colour == 'Y':
                colourList = listOfYellows
                appendcolourlist(colourList)
            elif colour == 'G':
                colourList = listOfGreens
                appendcolourlist(colourList)

    # Create the figures and plots the data
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(30, 10))

    ax1.axis([0, int(axis_width), 0, int(axis_height)])
    ax1.set_xlabel('X Displacement')
    ax1.set_ylabel('Y Displacement')
    ax1.plot(listOfReds[0], listOfReds[1], 'ro')
    ax1.plot(listOfYellows[0], listOfYellows[1], 'yo')
    ax1.plot(listOfGreens[0], listOfGreens[1], 'go')

    red_mean_displacement = sum(listOfReds[4]) / len(listOfReds[4])
    yellow_mean_displacement = sum(listOfYellows[4]) / len(listOfYellows[4])
    green_mean_displacement = sum(listOfGreens[4]) / len(listOfGreens[4])
    red_mean_velocity = sum(listOfReds[2]) / len(listOfReds[2])
    yellow_mean_velocity = sum(listOfYellows[2]) / len(listOfYellows[2])
    green_mean_velocity = sum(listOfGreens[2]) / len(listOfGreens[2])

    ax2.axis([0, max(listOfGreens[2]) + (float(max(listOfGreens[2])) * 0.1 ), 0, max(listOfGreens[4]) + (float(max(listOfGreens[4]) * 0.1))])
    ax2.set_xlabel('X Velocity (mm/s)')
    ax2.set_ylabel('Y Displacement')
    ax2.plot(listOfReds[2], listOfReds[4], 'ro')
    ax2.plot(listOfYellows[2], listOfYellows[4], 'yo')
    ax2.plot(listOfGreens[2], listOfGreens[4], 'go')

    # Plot the lines for the average displacement and the average velocities for each of the movmement profiles
    ax2.plot([0, 2000], [red_mean_displacement, red_mean_displacement], 'r--', linewidth=3)
    ax2.plot([0, 2000], [yellow_mean_displacement, yellow_mean_displacement], 'y--', linewidth=3)
    ax2.plot([0, 2000], [green_mean_displacement, green_mean_displacement], 'g--', linewidth=3)
    ax2.plot([red_mean_velocity, red_mean_velocity], [0, 2000], 'r--', linewidth=3)
    ax2.plot([yellow_mean_velocity, yellow_mean_velocity], [0, 2000], 'y--', linewidth=3)
    ax2.plot([green_mean_velocity , green_mean_velocity], [0, 2000], 'g--', linewidth=3)

    # Plot the exact points of average velocity and average displacement cross over
    ax2.plot([red_mean_velocity, red_mean_velocity], [red_mean_displacement, red_mean_displacement], 'ro', markersize =30)
    ax2.plot([yellow_mean_velocity, yellow_mean_velocity], [yellow_mean_displacement, yellow_mean_displacement], 'yo', markersize=30)
    ax2.plot([green_mean_velocity , green_mean_velocity], [green_mean_displacement, green_mean_displacement], 'go', markersize=30)

    xdata = [red_mean_velocity, yellow_mean_velocity, green_mean_velocity]
    ydata = [red_mean_displacement, yellow_mean_displacement, green_mean_displacement]

    popt, pcov = curve_fit(func, xdata, ydata)

    x = np.linspace(0, max(listOfGreens[2]) + (float(max(listOfGreens[2])) * 0.1), 100)
    y = func(x, popt[0], popt[1])
    ax2.plot(x,y, 'b', linewidth=3.0)

    red_integral = (quad(characteristic_equation, 0, red_mean_velocity))[0]
    yellow_integral = (quad(characteristic_equation, red_mean_velocity, yellow_mean_velocity))[0]
    green_integral = (quad(characteristic_equation, yellow_mean_velocity, green_mean_velocity))[0]

    red_coefficient = red_integral / red_integral
    yellow_coefficient = yellow_integral / red_integral
    green_coefficient = green_integral / red_integral

    #return red_coefficient, yellow_coefficient, green_coefficient

def move_to_dot_test_analysis():

    test_list = [[], [], [], [], [], [], [], []]
    accuracy_list = [[], []]

    for child in e[0]:

        frame = int(child.attrib['key'])
        xPosition = child.find('xPos').text
        yPosition = child.find('yPos').text
        xVelocity = child.find('xVel').text
        yVelocity = child.find('yVel').text
        colour = child.find('Colour').text
        XPosCurrentSpot = child.find('TransientTestData')[0].text
        YPosCurrentSpot = child.find('TransientTestData')[1].text
        distFromSpot = np.sqrt((np.square(float(XPosCurrentSpot) - float(xPosition)) +
                                np.square(float(YPosCurrentSpot) - float(yPosition))))
        velocityVector = np.sqrt(np.square(float(xVelocity)) + np.square(float(yVelocity)))

        test_list[0].append(float(xPosition))
        test_list[1].append(float(yPosition))
        test_list[2].append(float(xVelocity))
        test_list[3].append(float(yVelocity))
        test_list[4].append(int(XPosCurrentSpot))
        test_list[5].append(int(YPosCurrentSpot))
        test_list[6].append(distFromSpot)
        test_list[7].append(velocityVector)

        if distFromSpot <= boundary:
            accuracy_list[0].append(distFromSpot)
            accuracy_list[1].append(velocityVector)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(30, 10))

    ax1.axis([0, int(axis_width), 0, int(axis_height)])
    ax1.set_xlabel('X Displacement')
    ax1.set_ylabel('Y Displacement')
    ax1.plot(test_list[4], test_list[5], 'bo', markersize=boundary)
    ax1.plot(test_list[0], test_list[1], 'ro')

    ax2.axis([0, max(accuracy_list[0]) + 10.0, 0, max(accuracy_list[1]) + (float(max(accuracy_list[1])) * 0.1)])
    ax2.set_xlabel('Distance from Spot')
    ax2.set_ylabel('Velocity Vector')
    ax2.plot(accuracy_list[0], accuracy_list[1], 'ro')

    plt.show()







# Choose the XML data file to process
path = sys.argv[1]
e = xml.etree.ElementTree.parse(path).getroot()
#e = xml.etree.ElementTree.parse('tmp/XML_Server_Tx.xhtml').getroot()

# Unpack all of the Test Key data
test_subject_information = e[1]
test_information = e[2]
testee = test_subject_information[0].text
condition = test_subject_information[1].text
profession = test_subject_information[2].text
test = test_information[0].text
axis_height = test_information[1].text
axis_width = test_information[2].text
test_length = test_information[3].text
boundary = int(test_information[4].text)


if test == TestBuilder.switcher.get(0):

    coefficients = horizontal_line_test_analysis()
    print '\nThe Coefficients for that test are as follows:', coefficients
    updater = raw_input("\nType Y to update coeffcients. Otherwise press enter to view data\n")
    user_profile = Profiler(testee)
    if updater == 'Y':
        user_profile.write_linear_coefficients(coefficients)

elif test == TestBuilder.switcher.get(1):

    coefficients = vertical_line_test_analysis()
    print '\nThe Coefficients for that test are as follows:', coefficients
    updater = raw_input("\nType Y to update coeffcients. Otherwise press enter to view data\n")
    user_profile = Profiler(testee)
    if updater == 'Y':
        user_profile.write_vertical_coefficients(coefficients)

elif test == TestBuilder.switcher.get(2):

    diagonal_line_test_analysis()

elif test == TestBuilder.switcher.get(3):
    move_to_dot_test_analysis()

plt.show()