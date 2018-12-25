import numpy as np
import cv2
from collections import deque
import argparse
import atexit

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=8,help="max buffer size")
args = vars(ap.parse_args())


class VideoWatcher:

    def finishing(self):

        print "Exiting Video..."
        cv2.destroyAllWindows()
        self.cap.release()

    def __init__(self):

        self.cap = cv2.VideoCapture(0)
        self.ret, self.frame = self.cap.read()

        # take first frame of the video
        #ret, frame = cap.read()

        self.redLower = (45, 40, 40)
        self.redUpper = (90, 255, 255)

        self.pts = deque(maxlen=args["buffer"])
        self.counter = 0

        self.x = 0
        self.y = 0
        self.radius = 0
        self.direction = 0

        atexit.register(self.finishing)


    def video_tracker(self):

        self.ret, self.frame = self.cap.read()

        if self.ret == True:

            self.blurred = cv2.GaussianBlur(self.frame, (11, 11), 0)
            self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

            self.mask = cv2.inRange(self.hsv, self.redLower, self.redUpper)
            self.mask = cv2.erode(self.mask, None, iterations=1)
            self.mask = cv2.dilate(self.mask, None, iterations=2)

            self.cnts = cv2.findContours(self.mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            self.center = None

            if len(self.cnts) >= 1:

                self.c = max(self.cnts, key=cv2.contourArea)
                ((self.x, self.y), self.radius) = cv2.minEnclosingCircle(self.c)
                self.M = cv2.moments(self.c)
                if self.M["m00"] == 0.0:
                    self.M["m00"] = 1
                self.center = (int(self.M["m10"] / self.M["m00"]), int(self.M["m01"] / self.M["m00"]))

            if self.radius > 2:
                cv2.circle(self.frame, (int(self.x), int(self.y)), int(self.radius),
                            (0, 255, 255), 2)
                cv2.circle(self.frame, self.center, 5, (255, 0, 255), -1)
                self.pts.appendleft(self.center)

                for i in np.arange(1, len(self.pts)):

                    self.thickness = int(np.sqrt(args["buffer"] / float (i + 1)) * 2.5)
                    cv2.line(self.frame, self.pts[i - 1], self.pts[i], (0,0,255), self.thickness)

                self.xPos = '{0:.0f}'.format(self.x)
                self.yPos = '{0:.0f}'.format(self.y)
                cv2.putText(self.frame, "  X Position: " + self.xPos + "  Y Position: " + self.yPos, (10, self.frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)

                # Draw it on image
                # show the frame to our screen and increment the frame counter
                cv2.imshow("Frame", self.frame)
                #cv2.imshow("Mask", self.mask)

                self.key = cv2.waitKey(1) & 0xFF

                self.counter += 1

        return self.x, self.y