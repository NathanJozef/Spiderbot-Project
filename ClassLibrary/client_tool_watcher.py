import LeapControllers.leap as leap

def create():

    # Create a sample listener and controller
    listener = Client_Tool_Watcher
    controller = leap.Controller()
    controller.add_listener(listener)

class Client_Tool_Watcher(leap.Listener):

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

        self.xPos = tool.tip_position[0] + 250
        self.yPos = tool.tip_position[1] * (400/300)
        self.zPos = (tool.tip_position[2] + 250) * (400/300)

        #self.xPos = tool.tip_position[0]
        #self.yPos = tool.tip_position[1]
        #self.zPos = tool.tip_position[2]

        self.xVel = tool.tip_velocity[0]
        self.yVel = tool.tip_velocity[1]
        self.zVel = tool.tip_velocity[2]



    def modForLabView(self):

        self.xPos = ((self.xPos + 200) / 400) * 5
        if self.xPos > 4.9999:
           self.xPos = 4.99999
        elif self.xPos < 0.0001:
            self.xPos = 0.00111

        self.yPos = ((self.yPos) / 300) * 5
        if self.yPos > 4.9999:
            self.yPos = 4.99999
        elif self.yPos < 0.0001:
            self.yPos = 0.00111

        self.zPos = ((self.zPos + 120) / 320) * 5
        if self.zPos > 4.9999:
            self.zPos = 4.99999
        elif self.zPos < 0.0001:
            self.zPos = 0.00111

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
                #self.modForLabView()
                self.createCompString()

if __name__ == "__main__":
    create()