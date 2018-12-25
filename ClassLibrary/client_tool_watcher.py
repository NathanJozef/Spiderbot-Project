import LeapControllers.leap as leap
from ClassLibrary.tracker import VideoWatcher

def create():

    # Create a sample listener and controller
    listener = Client_Tool_Watcher
    controller = leap.Controller()
    controller.add_listener(listener)

class Client_Tool_Watcher(leap.Listener):

    def build_video(self):
        self.vid = VideoWatcher()

    def run_video(self):
        self.indX, self.indY = self.vid.video_tracker()
        return self.indX, self.indY

    def buildForUI(self):

        self.COUNTER = 0
        self.frame = str(self.COUNTER).zfill(10)
        self.xPos = 0
        self.yPos = 0
        self.zPos = 0
        self.xVel = 0
        self.yVel = 0
        self.zVel = 0
        self.xPressureLeft = str("Not Measured")
        self.xPressureRight = str("Not Measured")
        self.yPressureUp = str("Not Measured")
        self.yPressureDown = str("Not Measured")
        self.color = str("Not Applicable")

        ## For Accuracy Test
        #self.acc_counter = 0
        #self.acc_xPos = -200
        #self.direction_vector = 1

    def on_init(self, controller):
        print "Initialized Leap"

    def on_connect(self, controller):
        print "Connected to Leap"
        self.compString = "cli_0000000_0000000_0000000_0000000_0000000_0000000"

    def on_disconnect(self, controller):
        print "Disconnected Leap"

    def on_exit(self, controller):
        print "Exited"

    def grabData(self, tool):

        ## For accuracy test
        #print 'Acc Counter:', self.acc_counter
        #self.acc_counter += 1
        #if self.acc_counter % 400 == 0:
        #    self.acc_xPos += 20.0 * self.direction_vector

        #self.xPos = ((self.acc_xPos + 200) / 400) * 2 + 1.5
        #if self.xPos > 3.5:
        #    self.xPos = 3.5
        #    self.direction_vector = -1
        #elif self.xPos < 1.5:
        #    self.xPos = 1.5
        #    self.direction_vector = 1
        #self.xPos = str(self.xPos).zfill(7)
        #self.yPos = str(0.00000).zfill(7)
        #self.zPos = str(0.00000).zfill(7)

        # For UI Tests
        #self.xPos = tool.tip_position[0] + 250
        #self.yPos = tool.tip_position[1] * (400/300)
        #self.zPos = (tool.tip_position[2] + 250) * (400/300)

        # For normal control of digit with Leap
        self.xPos = tool.tip_position[0]
        self.yPos = tool.tip_position[1]
        self.zPos = tool.tip_position[2]
        self.xVel = tool.tip_velocity[0]
        self.yVel = tool.tip_velocity[1]
        self.zVel = tool.tip_velocity[2]


    def modForLabView(self):

        self.xPos = (((self.xPos + 200) / 400)) * 5
        if self.xPos > 4.99999:
           self.xPos = 4.99999
        elif self.xPos < 0.00011:
            self.xPos = 0.00011

        self.yPos = (((self.yPos) / 300) * 5) + 1.5
        if self.yPos > 4.99999:
            self.yPos = 4.99999
        elif self.yPos < 0.00011:
            self.yPos = 0.00011

        self.zPos = (((self.zPos + 120) / 320) * 5) + 1
        if self.zPos > 4.99999:
            self.zPos = 4.99999
        elif self.zPos < 0.00011:
            self.zPos = 0.00011

    def createCompString(self):

        xPosString = str(self.xPos)[0:7]
        yPosString = str(self.yPos)[0:7]
        zPosString = str(self.zPos)[0:7]
        xVelString = str(self.xVel)[0:7]
        yVelString = str(self.yVel)[0:7]
        zVelString = str(self.zVel)[0:7]

        self.compString = 'cli_' + xPosString + '_' \
                          + yPosString + '_' \
                          + zPosString + '_' \
                          + xVelString + '_' \
                          + yVelString + '_' \
                          + zVelString

    def on_frame(self, controller):

        # Get the most recent frame and report some basic information
        frame = controller.frame()

        for tool in frame.tools:

                self.grabData(tool)
                self.modForLabView()
                self.createCompString()

if __name__ == "__main__":
    create()