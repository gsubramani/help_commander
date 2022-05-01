from matplotlib.pyplot import pause
import pyqtgraph as pg
from helpplot import HelpPlot
from board01_etherent_connection import *


MY_IP_ADDRESS = '10.0.0.53'
BOARD_01_IP_ADDRESS = '10.0.0.45'



hEC = HelpEthernetConnection(MY_IP_ADDRESS)

axis = 0


hEC.send_parameter(axis, PARAMETER_CLEAR,0, 0);
hEC.send_parameter(axis, PARAMETER_TORQUE_CLAMP,0, 5.0)
hEC.send_parameter(axis, PARAMETER_VELOCITY_LIMIT,0, 5)
hEC.send_parameter(axis, PARAMETER_VELOCITY_DEADBAND,0, 0.1)


hEC.send_parameter(axis, PARAMETER_POSITION_GAIN,0, 50)
hEC.send_parameter(axis, PARAMETER_INTEGRATOR_GAIN,0, 2)
hEC.send_parameter(axis, PARAMETER_INTEGRATOR_CLAMP,0, 20)
hEC.send_parameter(axis, PARAMETER_DAMPING,0, 5)


hEC.send_parameter(axis, PARAMETER_INPUT_AMPLITUDE,0, 1)
hEC.send_parameter(axis, PARAMETER_INPUT_FREQUENCY,0, 0.0032)


hEC.send_parameter(axis, PARAMETER_INPUT_SETPOINT,0, 1)

hEC.send_parameter(axis, PARAMETER_CONTROLLER_MODE,0, MODE_POSITION_SIN_TRAJECTORY)


hEC.send_parameter(axis, PARAMETER_COMMIT,0, 0);



some_data = hEC.get_stream_data(128000)



hEC.send_parameter(axis, PARAMETER_CLEAR,0, 0);
hEC.send_parameter(axis, PARAMETER_TORQUE_CLAMP,0, 10.0)
hEC.send_parameter(axis, PARAMETER_VELOCITY_LIMIT,0, 1)

hEC.send_parameter(axis, PARAMETER_FRICTION_DITHER_RATE,0, 0)
hEC.send_parameter(axis, PARAMETER_FRICTION_FF_STATIC,0, 0)

hEC.send_parameter(axis, PARAMETER_POSITION_GAIN,0, 100)
hEC.send_parameter(axis, PARAMETER_INTEGRATOR_GAIN,0, 0.1)
hEC.send_parameter(axis, PARAMETER_INTEGRATOR_CLAMP,0, 20)
hEC.send_parameter(axis, PARAMETER_DAMPING,0, 3)

hEC.send_parameter(axis, PARAMETER_CONTROLLER_MODE,0, MODE_POSITION_CONSTANT)
hEC.send_parameter(axis, PARAMETER_INPUT_SETPOINT,0, 0.0)
hEC.send_parameter(axis, PARAMETER_COMMIT,0, 0);

pause(3)

hEC.send_parameter(axis, PARAMETER_TORQUE_CLAMP,0, 0.0)
hEC.send_parameter(axis, PARAMETER_CONTROLLER_MODE,0, MODE_IDLE)
hEC.send_parameter(axis, PARAMETER_COMMIT,0, 0);


hP  = HelpPlot(some_data[axis]['POSITION']['samples'], some_data[axis]['POSITION']['values'], row = 1, col = 1)
hP3 = HelpPlot(some_data[axis]['TORQUE']['samples'],   some_data[axis]['TORQUE']['values'],   row = 2, col = 1)
hP3 = HelpPlot(some_data[axis]['VELOCITY']['samples'], some_data[axis]['VELOCITY']['values'], row = 3, col = 1)

pg.exec()