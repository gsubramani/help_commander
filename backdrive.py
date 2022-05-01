from matplotlib.pyplot import pause
import pyqtgraph as pg
from helpplot import HelpPlot
from board01_etherent_connection import *


MY_IP_ADDRESS = '10.0.0.53'
BOARD_01_IP_ADDRESS = '10.0.0.45'



hEC = HelpEthernetConnection(MY_IP_ADDRESS)


def friction_comp(axis):
    global hEC
    # Safety
    hEC.send_parameter(axis, PARAMETER_CLEAR,0, 0);
    hEC.send_parameter(axis, PARAMETER_TORQUE_CLAMP,0, 20.0)
    hEC.send_parameter(axis, PARAMETER_VELOCITY_LIMIT,0, 3)

    # Turn off controller
    hEC.send_parameter(axis, PARAMETER_POSITION_GAIN,0, 0)
    hEC.send_parameter(axis, PARAMETER_INTEGRATOR_GAIN,0, 0)
    hEC.send_parameter(axis, PARAMETER_INTEGRATOR_CLAMP,0, 0)
    hEC.send_parameter(axis, PARAMETER_DAMPING,0, 0)
    hEC.send_parameter(axis, PARAMETER_VELOCITY_DEADBAND,0, 0)


    # Enabling friction compensation
    hEC.send_parameter(axis, PARAMETER_FRICTION_DITHER_RATE,0, 50)
    hEC.send_parameter(axis, PARAMETER_FRICTION_DITHER_BAND,0, 0.1)
    
    hEC.send_parameter(axis, PARAMETER_FRICTION_FF_KINETIC,0, 1)

    if(axis == 1):
        hEC.send_parameter(1, PARAMETER_FRICTION_FF_STATIC,0, 10)
        hEC.send_parameter(1, PARAMETER_FRICTION_FF_KINETIC,0, 1)
    else:
        hEC.send_parameter(0, PARAMETER_FRICTION_FF_STATIC,0, 10)
        hEC.send_parameter(0, PARAMETER_FRICTION_FF_KINETIC,0, 1)

    hEC.send_parameter(axis, PARAMETER_CONTROLLER_MODE,0, MODE_POSITION_CONSTANT)


    hEC.send_parameter(axis, PARAMETER_COMMIT,0, 0);


def deactivate_controller(axis):
    global hEC
    hEC.send_parameter(axis, PARAMETER_TORQUE_CLAMP,0, 0.0)
    hEC.send_parameter(axis, PARAMETER_CONTROLLER_MODE,0, MODE_IDLE)
    hEC.send_parameter(axis, PARAMETER_COMMIT,0, 0);


friction_comp(0)
pause(1)
friction_comp(1)

# some_data = hEC.get_stream_data(8000)
pause(20)

deactivate_controller(0)
pause(1)
deactivate_controller(1)

hP  = HelpPlot(some_data[0]['POSITION']['samples'], some_data[0]['POSITION']['values'], row = 1, col = 1)
hP3 = HelpPlot(some_data[0]['TORQUE']['samples'],   some_data[0]['TORQUE']['values'],   row = 2, col = 1)
hP3 = HelpPlot(some_data[0]['VELOCITY']['samples'], some_data[0]['VELOCITY']['values'], row = 3, col = 1)

pg.exec()