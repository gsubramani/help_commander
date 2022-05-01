# from matplotlib.pyplot import pause
# import pyqtgraph as pg
# from helpplot import HelpPlot
from board01_etherent_connection import *
import time


MY_IP_ADDRESS = '10.0.0.53'
BOARD_01_IP_ADDRESS = '10.0.0.45'



hEC = HelpEthernetConnection(MY_IP_ADDRESS)

axis = 1

hEC.append_request_data(axis, STATE_POSITION)
hEC.append_request_data(axis, STATE_VELOCITY)
hEC.append_request_data(axis, STATE_TORQUE)
answer = hEC.get_data_request()
print(answer)


# print(hEC.get_stream_data(100))

