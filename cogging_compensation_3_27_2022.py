# from tracemalloc import get_object_traceback
# from matplotlib.pyplot import pause
# import pyqtgraph as pg
# from helpplot import HelpPlot
# from typing import final
from board01_etherent_connection import *
import numpy as np
import time
import matplotlib.pyplot as plt
import pickle 
from setup_m1_controller import setup_m1_motor

MY_IP_ADDRESS = '10.0.0.53'
BOARD_01_IP_ADDRESS = '10.0.0.45'

hEC = HelpEthernetConnection(MY_IP_ADDRESS)

def goto_pos(axis, pos, tol = 0.001, timeout = 10, settle_time = 0.5, to_plot = False):
    global hEC
    setup_m1_motor(hEC);
    hEC.send_parameter(axis, PARAMETER_CLEAR,0, 0);
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
            print(current_pos, pos ,current_torque)
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
            
def get_pos_and_torque(axis):
    global hEC
    hEC.append_request_data(axis, STATE_POSITION)
    hEC.append_request_data(axis, STATE_TORQUE)
    result = hEC.get_data_request()
    pos = result['response_data'][0]
    torque = result['response_data'][1]
    return (pos, torque)

def collect_data(axis = 1, num_points = 10, file_name = "cogging_data.pkl"):

    goto_pos(axis, 0, to_plot=False)
    time.sleep(2)
    goto_pos(axis, 0, to_plot=False)
    time.sleep(2)
    input_positions = np.linspace(0,1,num_points)
    # input_positions2 = np.linspace(1,0,200)
    # input_positions = np.append(input_positions, input_positions2)

    # input_positions = np.random.rand(10)*0.05
    output_positions = []
    output_torques = []

    for pos in input_positions:
        goto_pos(axis, pos)
        pos, torque = get_pos_and_torque(axis)
        output_positions.append(pos)
        output_torques.append(torque)
        # goto_pos(axis, 0, settle_time = 0.1,tol = 0.002)
        
    print(output_positions, output_torques, input_positions - output_positions)
    data_to_pickle = {'input_positions' : input_positions,
                'output_positions' : output_positions,
                'output_torques' : output_torques
                } 
    pickle.dump( data_to_pickle,open(file_name,'wb'))


def analyse_data(file_name = "cogging_data.pkl"):
    data = pickle.load(open(file_name,'rb'))
    
    output_positions = data["output_positions"]
    output_torques = data["output_torques"]
    input_positions = data["input_positions"]
    
    plt.subplot(2,1,1)
    plt.plot(output_positions,output_torques,'.')
    plt.subplot(2,1,2)
    plt.plot(input_positions, abs(output_positions - input_positions), '.')
    plt.show()
    
    
if __name__ == "__main__":
    collect_data(axis = 1, num_points = 10, file_name = "cogging_data.pkl")
    analyse_data(file_name = "cogging_data.pkl")