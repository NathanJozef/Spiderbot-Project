

class SimpleLineTest:

    def __init__(self, ax, listener):

        self.listener = listener
        self.xData = [0]
        self.yData = [0]
        self.ax = ax
        self.ax.axis([0, 500, 0, 500])
        self.ax.plot([50, 450], [275, 275], linewidth=3.0, color='b')
        self.ax.plot([50, 450], [225, 225], linewidth=3.0, color='b')
        self.ax.plot([50, 450], [250, 250], '--', linewidth=1.0, color='b')
        self.point = self.ax.plot(self.xData, self.yData, 'ro', markersize=10)

    def update(self, list):

        self.ax.lines.remove(self.ax.lines[3])
        self.xData[0] = list[0]
        self.yData[0] = list[1]

        #  Set the colour of the indicator to inform the user of the speed to generate
        if self.listener._COUNTER < 400:
            self.listener.color = 'R'
            self.ax.plot(self.xData, self.yData, 'ro', markersize=10)
        elif 400 <= self.listener._COUNTER < 800:
            self.listener.color = 'Y'
            self.ax.plot(self.xData, self.yData, 'yo', markersize=10)
        elif 800 <= self.listener._COUNTER < 1200:
            self.listener.color = 'G'
            self.ax.plot(self.xData, self.yData, 'go', markersize=10)
        elif self.listener._COUNTER >= 1200:
            quit()

        return self

