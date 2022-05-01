from matplotlib.pyplot import pause
import pyqtgraph as pg
from helpplot import HelpPlot
from board01_etherent_connection import *


MY_IP_ADDRESS = '10.0.0.53'
BOARD_01_IP_ADDRESS = '10.0.0.45'



hEC = HelpEthernetConnection(MY_IP_ADDRESS)

axis = 1

some_data = hEC.get_stream_data(16000,clear_old = False)



hP  = HelpPlot(some_data[axis]['POSITION']['samples'], some_data[axis]['POSITION']['values'], row = 1, col = 1)
hP3 = HelpPlot(some_data[axis]['TORQUE']['samples'],   some_data[axis]['TORQUE']['values'],   row = 2, col = 1)
hP3 = HelpPlot(some_data[axis]['VELOCITY']['samples'], some_data[axis]['VELOCITY']['values'], row = 3, col = 1)

pg.exec()