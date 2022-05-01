from matplotlib.pyplot import pause
import pyqtgraph as pg
from helpplot import HelpPlot
from board01_etherent_connection import *


MY_IP_ADDRESS = '10.0.0.53'
BOARD_01_IP_ADDRESS = '10.0.0.45'



hEC = HelpEthernetConnection(MY_IP_ADDRESS)



hEC.send_parameter(0, PARAMETER_CLEAR,0, 0);

hEC.send_parameter(0, PARAMETER_TORQUE_CLAMP,0, 10.0)
hEC.send_parameter(0, PARAMETER_INPUT_AMPLITUDE,0, 10.0)
hEC.send_parameter(0, PARAMETER_INPUT_FREQUENCY,0, 1)
hEC.send_parameter(0, PARAMETER_VELOCITY_LIMIT,0, 0.3)

hEC.send_parameter(0, PARAMETER_CONTROLLER_MODE,0, MODE_TORQUE_RAMP);
hEC.send_parameter(0, PARAMETER_COMMIT,0, 0);



some_data = hEC.get_stream_data(128000)


hEC.send_parameter(0, PARAMETER_TORQUE_CLAMP,0, 0.0)
hEC.send_parameter(0, PARAMETER_CONTROLLER_MODE,0, MODE_IDLE)
hEC.send_parameter(0, PARAMETER_COMMIT,0, 0);

hP  = HelpPlot(some_data[0]['POSITION']['samples'], some_data[0]['POSITION']['values'], row = 1, col = 1)
hP3 = HelpPlot(some_data[0]['TORQUE']['samples'],   some_data[0]['TORQUE']['values'],   row = 2, col = 1)
hP3 = HelpPlot(some_data[0]['VELOCITY']['samples'], some_data[0]['VELOCITY']['values'], row = 3, col = 1)

pg.exec()
