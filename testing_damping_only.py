from matplotlib.pyplot import pause
# import pyqtgraph as pg
# from helpplot import HelpPlot
from board01_etherent_connection import *


MY_IP_ADDRESS = '10.0.0.53'
BOARD_01_IP_ADDRESS = '10.0.0.45'



hEC = HelpEthernetConnection(MY_IP_ADDRESS)


def damping_only(axis):
    global hEC
    # Safety
    hEC.send_parameter(axis, PARAMETER_CLEAR,0, 0);
    hEC.send_parameter(axis, PARAMETER_TORQUE_CLAMP,0, 5.0)
    hEC.send_parameter(axis, PARAMETER_VELOCITY_LIMIT,0, 5)

    # Turn off controller
    hEC.send_parameter(axis, PARAMETER_POSITION_GAIN,0, 0)
    hEC.send_parameter(axis, PARAMETER_INTEGRATOR_GAIN,0, 0)
    hEC.send_parameter(axis, PARAMETER_INTEGRATOR_CLAMP,0, 0)
    
    hEC.send_parameter(axis, PARAMETER_DAMPING,0, 1)
    hEC.send_parameter(axis, PARAMETER_VELOCITY_DEADBAND,0, 0.2)



    hEC.send_parameter(axis, PARAMETER_FRICTION_DITHER_RATE,0, 0)
    hEC.send_parameter(axis, PARAMETER_FRICTION_DITHER_BAND,0, 0)
    
    hEC.send_parameter(axis, PARAMETER_FRICTION_FF_KINETIC,0, 0)

    hEC.send_parameter(axis, PARAMETER_FRICTION_FF_STATIC,0, 0)
    hEC.send_parameter(axis, PARAMETER_FRICTION_FF_KINETIC,0, 0)

    hEC.send_parameter(axis, PARAMETER_CONTROLLER_MODE,0, MODE_POSITION_CONSTANT)
    
    hEC.send_parameter(axis, PARAMETER_COMMIT,0, 0);


def deactivate_controller(axis):
    global hEC
    hEC.send_parameter(axis, PARAMETER_TORQUE_CLAMP,0, 0.0)
    hEC.send_parameter(axis, PARAMETER_CONTROLLER_MODE,0, MODE_IDLE)
    hEC.send_parameter(axis, PARAMETER_COMMIT,0, 0);


damping_only(1)
# deactivate_controller(0)
