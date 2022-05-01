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

hEC = HelpEthernetConnection(MY_IP_ADDRESS)


def goto_pos(axis, pos, tol = 0.001, timeout = 2, settle_time = 1, to_plot = False):
    global hEC
    hEC.send_parameter(axis, PARAMETER_CLEAR,0, 0);
    hEC.send_parameter(axis, PARAMETER_TORQUE_CLAMP,0, 0.0)
    hEC.send_parameter(axis, PARAMETER_VELOCITY_LIMIT,0, 5)
    hEC.send_parameter(axis, PARAMETER_VELOCITY_DEADBAND,0, 0.1)


    hEC.send_parameter(axis, PARAMETER_POSITION_GAIN,0, 25.0)
    hEC.send_parameter(axis, PARAMETER_INTEGRATOR_GAIN,0, 1.0)
    
    hEC.send_parameter(axis, PARAMETER_INTEGRATOR_CLAMP,0, 2.5)
    hEC.send_parameter(axis, PARAMETER_DAMPING,0, 5.0)

    hEC.send_parameter(axis, PARAMETER_INPUT_SETPOINT,0, pos)
    hEC.send_parameter(axis, PARAMETER_CONTROLLER_MODE,0, MODE_POSITION_CONSTANT)

    hEC.send_parameter(axis, PARAMETER_COMMIT,0, 0);
    
    start_time = time.time()
    settling_start_time = time.time()

    pos_trajectory = []
    torque_command = []

    while True: 
        if(time.time() - start_time > timeout):
            break

        hEC.append_request_data(1, STATE_POSITION)
        hEC.append_request_data(1, STATE_TORQUE)
        
        
        try:
            result = hEC.get_data_request()
            current_pos = result['response_data'][0]
            current_torque = result['response_data'][1]
            print(current_pos, current_torque)
            pos_trajectory.append(current_pos)
            torque_command.append(current_torque)
        except:
            continue
            
        if(np.abs(current_pos - pos)  > tol):
            settling_start_time = time.time()
        else:
            if(time.time() - settling_start_time > settle_time):
                print("reached pos with error:",  current_pos - pos)
                break
    if(to_plot):
        plt.subplot(2,1,1)
        plt.plot(pos_trajectory)
        plt.subplot(2,1,2)
        plt.plot(torque_command)
        plt.show()
            
            
goto_pos(1,0.0, to_plot = False)
time.sleep(1)            
goto_pos(1,0.1, to_plot = True)
time.sleep(1)           
goto_pos(1,0.0)