import pickle

class server_data_handler:

    _COUNTER = 0

    def __init__(self):

        server_data_handler._COUNTER += 1

        self.frame = str(self._COUNTER).zfill(10)

        self.xPressureLeft = str("Not Measured")
        self.xPressureRight = str("Not Measured")
        self.yPressureUp = str("Not Measured")
        self.yPressureDown = str("Not Measured")
        self.color = str("R")

    def __str__(self):

        return "TECHNICAL TEST:" + self.frame + "\n" + \
               "x Position: " + str(self.xPos) + "\n" + \
               "y Position: " + str(self.yPos) + "\n" + \
               "z Position: " + str(self.zPos) + "\n" + \
               "x Velocity: " + str(self.xVel) + "\n" + \
               "y Velocity: " + str(self.yVel) + "\n" + \
               "z Velocity: " + str(self.zVel) + "\n" + \
               "x Pressure Left: " + str(self.xPressureLeft) + "\n" + \
               "x Pressure Right: " + str(self.xPressureRight) + "\n" + \
               "y Pressure Up: " + str(self.yPressureUp) + "\n" + \
               "y Pressure Down: " + str(self.yPressureDown)

    def append_leapdata(self, data_dump):

        split_data = data_dump.split("_")

        self.xPos = split_data[1]
        self.yPos = split_data[2]
        self.zPos = split_data[3]
        self.xVel = split_data[4]
        self.yVel = split_data[5]
        self.zVel = split_data[6]

        self.pickle_object("tmp/leap_data_pickle")

    def append_pressures(self, data_dump):

        split_data = data_dump.split("_")

        self.xPressureLeft = str(split_data[1]).strip().zfill(7)
        self.xPressureRight = str(split_data[2]).strip().zfill(7)
        self.yPressureUp = str(split_data[3]).strip().zfill(7)
        self.yPressureDown = str(split_data[4]).strip().zfill(7)

        self.pickle_object("tmp/LabView_data_pickle")

    def pickle_data_for_LabView(self):

        self.frame = str(int(self.frame) / 2).zfill(10)
        picklefile = open("tmp/smallPickle", 'wb')
        pickle_string = self.frame + "_" + self.xPos + "_" + self.yPos + "_" + self.zPos
        pickle.dump(pickle_string, picklefile)
        picklefile.close()

    def unpickle_data_for_Labview(self):

        picklefile = open("tmp/smallPickle", 'rb')
        LabView_Pos_String = pickle.load(picklefile)
        picklefile.close()

        return LabView_Pos_String


    def pickle_object(self, filename):

        leappickle = open(filename, 'wb')
        pickle.dump(self, leappickle)
        leappickle.close()



