from unittest import main
from matplotlib.pyplot import pause
import matplotlib.pyplot as plt
# import pyqtgraph as pg
# from helpplot import HelpPlot
from board01_etherent_connection import *
import numpy as np
import pickle
from scipy import signal

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
    


def collect_data(file_name = "sensor_delay.pkl"):
    hEC = HelpEthernetConnection(MY_IP_ADDRESS)
    
    command_sinusoidal_torque(hEC,axis = axis, amplitude= 5, frequency=100)
    pause(1)
    some_data = hEC.get_stream_data(8000, clear_old=True)
    pause(1)
    clamp_torque(hEC, axis = axis)
    
    pickle.dump(some_data,open(file_name,'wb')) 


def get_fft_signal(signal, time_step = 0.001):
    n = len(signal)
    window = np.blackman(n)
    signal_w = window*signal/np.mean(signal)
    signal_fft = np.fft.fft(signal_w)
    ws = np.fft.fftfreq(n, d=time_step)
    
    signal_fft = signal_fft[ws > 0];
    ws = ws[ws > 0]
    
    return (signal_fft, ws)
    
    

def analyse_data(file_name = "sensor_delay.pkl"):
    some_data = pickle.load(open(file_name,'rb'))
    
    position = np.array(some_data[axis]['POSITION']['values'])
    position_t = np.array(some_data[axis]['POSITION']['samples'])
    
    torque_back = np.array(some_data[axis]['VELOCITY']['values'])
    torque_back_t = np.array(some_data[axis]['VELOCITY']['samples']) # torque is proxied in on the odrive now
    
    torque = np.array(some_data[axis]['TORQUE']['values'])
    torque_t = np.array(some_data[axis]['TORQUE']['samples'])


    b, a = signal.butter(4, 6, 'high', fs = 1000)
    position = signal.filtfilt(b, a, position);
    # torque = signal.filtfilt(b, a, torque);
    
    
    # f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    # ax1.plot(torque,'g')
    # ax2.plot(position,'r')
    
    torque_normalized = np.array(torque)/max(torque)
    position_normalized = np.array(position)/max(position)
    torque_back_normalized = np.array(torque_back)/max(torque_back)


    pos_peaks = signal.find_peaks(position_normalized, distance = 80)[0].tolist()
    torque_peaks = signal.find_peaks(torque_normalized, distance = 80)[0].tolist()
    
    
    plt.figure()
    plt.plot(torque_t,torque_normalized ,'g')
    plt.plot(torque_t[torque_peaks], torque_normalized[torque_peaks], '*g')
    
    plt.plot(position_t,position_normalized,'r')
    plt.plot(position_t[pos_peaks], position_normalized[pos_peaks], '*r')
    
    
    plt.show()
    
    plt.figure()
    plt.plot(torque_back_t - min(torque_back_t),torque_back_normalized,'b' )
    plt.plot(torque_t- min(torque_back_t),torque_normalized,'g' )    
    plt.show()
    
    n = min(len(pos_peaks), len(torque_peaks))
    
    
    mean_delay_samples = np.average(position_t[pos_peaks[:n]] - torque_t[torque_peaks[:n]])
    print(mean_delay_samples)


if __name__ == "__main__":
    collect_data(file_name="sensor_delay10_4kbwHZ.pkl")
    analyse_data(file_name="sensor_delay10_4kbwHZ.pkl")
    