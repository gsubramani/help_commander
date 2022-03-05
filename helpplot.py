
from time import sleep

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from time import perf_counter
import numpy as np

class HelpPlot:

    win = pg.GraphicsLayoutWidget(show=True)
    win.setWindowTitle('Help Plots')

    def __init__(self, x, y, curve = None, subplot = None, row = None, col = None, pen = pg.mkPen('b', width=2)):

        if(subplot is None):
            if(row == None or col == None):
                self.subplot = self.win.addPlot()
            else:
                self.subplot = self.win.addPlot(row=row, col=col)
            self.curve = self.subplot.plot(x, y, pen = pen)
            return

        else:
            self.subplot = subplot

        if(curve is None):
            self.curve = self.subplot.plot(x, y, pen = pen)
        else:
            self.subplot.plot(x,y, pen = pen)
        return




# timer = pg.QtCore.QTimer()
# timer.timeout.connect(update)
# timer.start(1)
#
# pg.exec()
