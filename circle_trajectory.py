from matplotlib.pyplot import pause
import pyqtgraph as pg
from helpplot import HelpPlot
from board01_etherent_connection import HelpEthernetConnection


MY_IP_ADDRESS = '10.0.0.53'
BOARD_01_IP_ADDRESS = '10.0.0.45'


PARAMETER_POSITION_GAIN = 10 
PARAMETER_VELOCITY_GAIN = 11
PARAMETER_INTEGRATOR_GAIN = 12

PARAMETER_INTEGRATOR_CLAMP = 13
PARAMETER_TORQUE_CLAMP = 14
PARAMETER_INPUT_SETPOINT = 15

PARAMETER_DAMPING    = 16

PARAMETER_0 = 20
PARAMETER_1 = 21
PARAMETER_2 = 22
PARAMETER_3 = 23
PARAMETER_4 = 24
PARAMETER_5 = 25
PARAMETER_6 = 26
PARAMETER_7 = 27
PARAMETER_8 = 28
PARAMETER_9 = 29



hEC = HelpEthernetConnection(MY_IP_ADDRESS)




hEC.send_parameter(0, PARAMETER_INTEGRATOR_GAIN, 10);
hEC.send_parameter(0, PARAMETER_POSITION_GAIN,   100);
hEC.send_parameter(0, PARAMETER_DAMPING, 3);

hEC.send_parameter(0, PARAMETER_INPUT_SETPOINT, 0.5);

hEC.send_parameter(0, PARAMETER_TORQUE_CLAMP, 10.0);

steps = 360
distance = 1

for ii in range(steps):
    hEC.send_parameter(0, PARAMETER_INPUT_SETPOINT, ii/steps * distance)
    pause(0.1)

for ii in range(steps):
    hEC.send_parameter(0, PARAMETER_INPUT_SETPOINT, distance - ii/steps* distance)  
    pause(0.1)


hEC.send_parameter(0, PARAMETER_TORQUE_CLAMP, 0.0)


# some_data = hEC.get_structured_data(2000)
# hP  = HelpPlot(some_data[0]['POSITION']['samples'], some_data[0]['POSITION']['values'], row = 1, col = 1)
# hP3 = HelpPlot(some_data[0]['TORQUE']['samples'],   some_data[0]['TORQUE']['values'],   row = 2, col = 1)
# hP3 = HelpPlot(some_data[0]['VELOCITY']['samples'], some_data[0]['VELOCITY']['values'], row = 3, col = 1)

# pg.exec()

# # reset back to nominal values
# hEC.send_parameter(0, PARAMETER_INTEGRATOR_GAIN, 5);
# hEC.send_parameter(0, PARAMETER_POSITION_GAIN,   40);
# hEC.send_parameter(0, PARAMETER_DAMPING, 1);

# hEC.send_parameter(0, PARAMETER_INPUT_SETPOINT, 0.0);

# pause(1)

# hEC.send_parameter(0, PARAMETER_TORQUE_CLAMP, 0.0);

