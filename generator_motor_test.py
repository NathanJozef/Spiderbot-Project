import matplotlib.pyplot as plt
import matplotlib.animation as animation
import ClassLibrary.motor_tests as mt
from ClassLibrary.client_tool_watcher import Client_Tool_Watcher
from LeapControllers.leap import Controller

def generator(test_instance):

    #  Create the connection to the leap controller
    listener = Client_Tool_Watcher()
    listener.buildForUI()  # Initiate the leap listener for use with the graphing software
    controller = Controller()
    controller.add_listener(listener)

    class Scope:

        # Create the initial test
        def __init__(self, ax, listener, test_instance):

            if test_instance.testtype == 0:
                self.test = mt.Horizontal_Line_Test(ax, listener, test_instance)
            elif test_instance.testtype == 1:
                self.test = mt.Vertical_Line_Test(ax, listener, test_instance)
            elif test_instance.testtype == 2:
                self.test = mt.Diagonal_Line_Validation(ax, listener, test_instance)
            elif test_instance.testtype == 3:
                self.test = mt.Accuracy_Test(ax, listener, test_instance)

        def update(self, postion_corodinates):

            return self.test.update(postion_corodinates)


    def emitter():

        while True:
            listener.COUNTER += + 1
            listener.frame = str(listener.COUNTER).zfill(10)
            position_coordinates = [listener.xPos, listener.yPos]
            yield position_coordinates

    fig, ax = plt.subplots(figsize=(10,10))
    ax.axis([0, 500, 500, 0])

    scope = Scope(ax, listener, test_instance)

    ani = animation.FuncAnimation(fig, scope.update, emitter, interval=10, blit=False)

    plt.show()
