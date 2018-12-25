import xml.etree.ElementTree
import matplotlib.pyplot as plt
import numpy as np
import sys
from mpl_toolkits.mplot3d import Axes3D



framelist = []
xPosList = []
indicatedXlist = []
indicatedYlist = []
XListQueue = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
YListQueue = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
i = 0
sens = 30

# Choose the XML data file to process
path = sys.argv[1]
e = xml.etree.ElementTree.parse(path).getroot()

def add_to_list(a, b, c, d):

    framelist.append(a)
    xPosList.append(b)
    indicatedXlist.append(c)
    indicatedYlist.append(d)

for child in e[0]:

    frame = (int(child.attrib['key']))
    xPos = (float(child.find('xPos').text))
    indicatedX = (int(child.find('IndicatedValues').find('IndicatedX').text))
    indicatedY = (500 - int(child.find('IndicatedValues').find('IndicatedY').text))
    XListQueue.pop(0)
    XListQueue.append(float(indicatedX))
    YListQueue.pop(0)
    YListQueue.append(float(indicatedY))

    if i < 10:

        add_to_list(frame, xPos, indicatedX, indicatedY)

    elif sum(XListQueue)/len(XListQueue) - sens <= indicatedX <= sum(XListQueue)/len(XListQueue) + sens \
            and sum(YListQueue)/len(YListQueue) - sens <= indicatedY <= sum(YListQueue)/len(YListQueue) + sens:

        add_to_list(frame, xPos, indicatedX, indicatedY)

    i += 1


# Create the figures and plots the data
fig = plt.figure(figsize=(13, 13))

#ax1 = fig.add_subplot(3,1,1)
#ax1.set_xlabel('X Coordinate')
#ax1.set_ylabel('Y Coordinate')
#ax1.plot(indicatedXlist, indicatedYlist, 'ro')
#ax1.set_xlim([0,600])
#ax1.set_ylim([0,500])

#ax2 = fig.add_subplot(3,1,2)
#ax2.set_xlabel('X Coordinate')
#ax2.set_ylabel('Input Coordinate')
#ax2.plot(indicatedXlist, xPosList, 'g+')
#ax2.set_xlim([0,600])
#ax2.set_ylim([0,5])

#ax3 = fig.add_subplot(3,1,3)
#ax3.set_xlabel('Y Coordinate')
#ax3.set_ylabel('Input Coordinate')
#ax3.plot(indicatedYlist, xPosList, 'b+')
#ax3.set_xlim([0,500])
#ax3.set_ylim([0,5])

ax2 = fig.add_subplot(1,1,1, projection='3d')
ax2.set_title('Digit Movement Against Input Coordinate')
ax2.set_xlabel('X Coordinate')
ax2.set_ylabel('Y Coordinate')
ax2.set_zlabel('Input Coordinate')
ax2.plot(indicatedXlist, indicatedYlist, 'r+', zdir='z', zs=0)
ax2.plot(indicatedXlist, xPosList, 'g+', zdir='y', zs=500)
ax2.plot(indicatedYlist, xPosList, 'b+', zdir='x', zs=0)
ax2.scatter(indicatedXlist, indicatedYlist, xPosList, c='r', marker='o')

ax2.set_xlim([0,600])
ax2.set_ylim([0,500])
ax2.set_zlim([0,5])

plt.show()