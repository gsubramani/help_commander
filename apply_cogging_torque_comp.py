# from tracemalloc import get_object_traceback
# from matplotlib.pyplot import pause
# import pyqtgraph as pg
# from helpplot import HelpPlot
from typing import final
from board01_etherent_connection import *
import numpy as np
import time
import matplotlib.pyplot as plt
import pickle 


MY_IP_ADDRESS = '10.0.0.53'
BOARD_01_IP_ADDRESS = '10.0.0.45'

cogging_torque_values = pickle.load(open("cogging_torque_compensation_values.pkl",'rb'))

hEC = HelpEthernetConnection(MY_IP_ADDRESS)

axis = 1

hEC.send_parameter(axis, PARAMETER_CLEAR,0, 0);
hEC.send_parameter(axis, PARAMETER_TORQUE_CLAMP,0, 4.0)
hEC.send_parameter(axis, PARAMETER_VELOCITY_LIMIT,0, 3)
hEC.send_parameter(axis, PARAMETER_VELOCITY_DEADBAND,0, 0.0)

hEC.send_parameter(axis, PARAMETER_FRICTION_DITHER_BAND, 0, 0.02)
hEC.send_parameter(axis, PARAMETER_FRICTION_DITHER_RATE, 0, 0)

hEC.send_parameter(axis, PARAMETER_FRICTION_FF_STATIC, 0, 0.0)
hEC.send_parameter(axis, PARAMETER_FRICTION_FF_KINETIC, 0, 0.0)



hEC.send_parameter(axis, PARAMETER_POSITION_GAIN,0, 0.0)
hEC.send_parameter(axis, PARAMETER_INTEGRATOR_GAIN,0, 0.0)

hEC.send_parameter(axis, PARAMETER_INTEGRATOR_CLAMP,0, 0)
hEC.send_parameter(axis, PARAMETER_DAMPING,0, 0.0)

hEC.send_parameter(axis, PARAMETER_INPUT_SETPOINT,0, 0)
hEC.send_parameter(axis, PARAMETER_CONTROLLER_MODE,0, MODE_POSITION_CONSTANT)
hEC.send_parameter(axis, PARAMETER_COMMIT,0, 0);



hEC.send_parameter(axis, PARAMETER_CLEAR,0, 0);
print(cogging_torque_values)
for ind, cogging in enumerate(cogging_torque_values):
    hEC.send_parameter(axis, PARAMETER_COGGING_FF_TORQUE, ind, cogging);
    
hEC.send_parameter(axis, PARAMETER_COMMIT,0, 0)

