from unittest import main
from matplotlib.pyplot import pause
import matplotlib.pyplot as plt
# import pyqtgraph as pg
# from helpplot import HelpPlot
from board01_etherent_connection import *
import numpy as np
import pickle

MY_IP_ADDRESS = '10.0.0.53'
BOARD_01_IP_ADDRESS = '10.0.0.45'




axis = 1

def command_sinusoidal_torque(hEC, axis = 1, amplitude = 1, frequency = 1):
    hEC.send_parameter(axis, PARAMETER_CLEAR,0, 0);
    hEC.send_parameter(axis, PARAMETER_TORQUE_CLAMP,0, 10.0)
    hEC.send_parameter(axis, PARAMETER_VELOCITY_LIMIT,0, 20)
    hEC.send_parameter(axis, PARAMETER_VELOCITY_DEADBAND,0, 0.0)
    hEC.send_parameter(axis, PARAMETER_INPUT_AMPLITUDE,0, amplitude)
    hEC.send_parameter(axis, PARAMETER_INPUT_FREQUENCY,0, frequency)
    hEC.send_parameter(axis, PARAMETER_CONTROLLER_MODE,0, MODE_TORQUE_SIN_TRAJECTORY)
    hEC.send_parameter(axis, PARAMETER_COMMIT,0, 0);    

def clamp_torque(hEC, axis = 1):
    hEC.send_parameter(axis, PARAMETER_CLEAR,0, 0);
    hEC.send_parameter(axis, PARAMETER_INPUT_AMPLITUDE,0, 0)
    hEC.send_parameter(axis, PARAMETER_INPUT_FREQUENCY,0, 0)
    hEC.send_parameter(axis, PARAMETER_TORQUE_CLAMP,0, 0.0)
    hEC.send_parameter(axis, PARAMETER_COMMIT,0, 0);    
    


def collect_data(num_points = 2, start_pow = 1, end_pow = 2, file_name = "frequency_response1_4_3_2022.pkl"):
    hEC = HelpEthernetConnection(MY_IP_ADDRESS)

    freqs = 10**(np.linspace(start_pow,end_pow,num_points))

    data_collection = []

    for frequency in freqs:
        command_sinusoidal_torque(hEC,axis = axis, amplitude= 3, frequency=frequency)
        pause(1)
        some_data = hEC.get_stream_data(64000, clear_old=True)
        pause(1)
        clamp_torque(hEC, axis = axis)
        data_collection.append({'frequency':frequency ,'data': some_data})
        
    pickle.dump(data_collection,open(file_name,'wb')) 

# hP  = HelpPlot(some_data[axis]['POSITION']['samples'], some_data[axis]['POSITION']['values'], row = 1, col = 1)
# hP3 = HelpPlot(some_data[axis]['TORQUE']['samples'],   some_data[axis]['TORQUE']['values'],   row = 2, col = 1)
# hP3 = HelpPlot(some_data[axis]['VELOCITY']['samples'], some_data[axis]['VELOCITY']['values'], row = 3, col = 1)

# pg.exec()

def get_fft_signal(signal, time_step = 0.001):
    n = len(signal)
    window = np.blackman(n)
    signal_w = window*signal/np.mean(signal)
    signal_fft = np.fft.fft(signal_w)
    ws = np.fft.fftfreq(n, d=time_step)
    
    signal_fft = signal_fft[ws > 0];
    ws = ws[ws > 0]
    
    return (signal_fft, ws)
    
    

def analyse_data(file_name = "frequency_response1_4_3_2022.pkl"):
    data_collection = pickle.load(open(file_name,'rb'))
    
    axis = 1
    
    frf_pos = []
    frf_tor = []
    frf_w = []
    
    for data_set in data_collection:
        data = data_set['data']
        frequency =data_set['frequency']
        
        position = data[axis]['POSITION']['values']
        torque = data[axis]['TORQUE']['values']
        
        fposition, wp = get_fft_signal(position)        
        ftorque, wt = get_fft_signal(torque)
    
        f_ind = np.argmax(np.absolute(ftorque))

        frf_tor.append(ftorque[f_ind])
        frf_pos.append(fposition[f_ind])
        frf_w.append(wt[f_ind])
         
        

        # plot_start = 8
        # plt.subplot(3,1,1)
        # plt.plot(wp[plot_start:],fposition[plot_start:])
        # plt.subplot(3,1,2)
        # plt.plot(wt[plot_start:], ftorque[plot_start:])
        # plt.subplot(3,1,3)
        # plt.plot(wt[plot_start:], fposition[plot_start:]/ftorque[plot_start:])

    frf = np.array(frf_pos)/np.array(frf_tor)
    plt.loglog(np.array(frf_w), np.absolute(frf), )
    plt.show()          


if __name__ == "__main__":
    # collect_data(num_points=10, start_pow = 0, end_pow = 1.7)
    analyse_data()
    