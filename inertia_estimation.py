from board01_etherent_connection import *
import control
from board01_etherent_connection import *
from board01_helper_functions import *
from setup_m1_controller import *
import pickle
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np


MY_IP_ADDRESS = '10.0.0.53'
BOARD_01_IP_ADDRESS = '10.0.0.45'

def collect_data(axis = 1, num_points = 10, start_pow = 0, end_pow = 2, amplitude = 3, file_name = "inertia_estimation.pkl"):
    hEC = HelpEthernetConnection(MY_IP_ADDRESS)
    freqs = 10**(np.linspace(start_pow,end_pow,num_points))

    data_collection = []

    for frequency in freqs:
        command_sinusoidal_torque(hEC,axis = axis, amplitude = amplitude, frequency=frequency)
        pause(1)
        some_data = hEC.get_stream_data(64000, clear_old=True)
        pause(1)
        clamp_torque(hEC, axis = axis)
        data_collection.append({'frequency':frequency ,
                                'data': some_data,
                                'amplitude': amplitude})
        
    pickle.dump(data_collection,open(file_name,'wb'))
    
    
def analyse_data(axis = 1, file_name = "inertia_estimation.pkl"):
    
    data_collection = pickle.load(open(file_name,'rb'))

    max_poses = []
    max_torques = []
    amplitudes = []
    frequencies = []
    
    
    for data_dict in data_collection:
        frequency = data_dict['frequency']
        data = data_dict['data']
        amplitudes.append(data_dict['amplitude'])
        frequencies.append(frequency)
        
        position_ = np.array(data[axis]['POSITION']['values'])
        # position_t = np.array(data[axis]['POSITION']['samples'])        
        
        torque = np.array(data[axis]['TORQUE']['values'])
        # torque_t = np.array(data[axis]['TORQUE']['samples'])
                
        b, a = signal.butter(4, frequency/2, 'high', fs = 1000)
        position = signal.filtfilt(b, a, position_);
        
        # K = 10
        # tf_acc = control.tf([K*K,0,0],[1,2*K, K*K]);
        # tf_acc_disc = control.sample_system(tf_acc, 0.001, method='bilinear');

        # acceleration = signal.filtfilt(tf_acc_disc.num[0][0], tf_acc_disc.den[0][0], position_)
        
        # cog = torque[:-1] + acceleration*0.0326

        # plt.subplot(3,1,1)
        # plt.plot(acceleration, 'r')
        # plt.subplot(3,1,2)
        # plt.plot(position_, 'g')
        # plt.subplot(3,1,3)
        # plt.plot(cog,'b')        
        # plt.show()

        max_pos = np.max(np.abs(position))
        max_torque = np.max(np.abs(torque))

        max_poses.append(max_pos)
        max_torques.append(max_torque)

    max_poses = np.array(max_poses)
    max_torques = np.array(max_torques)
    amplitudes = np.array(amplitudes)
    frequencies = np.array(frequencies)
    
    
    Kt = 1
    inertias = max_torques*Kt/(2*np.pi*frequencies)**2/max_poses
    
    plt.subplot(3,1,1)
    plt.plot(max_poses, '.')

    plt.subplot(3,1,2)
    plt.plot(max_torques, '.')
    
    plt.subplot(3,1,3)
    plt.plot(inertias,'.')
    plt.show()
    
    print(np.median(inertias))




        
if __name__ == "__main__":
    # collect_data(num_points = 10, start_pow = 0, end_pow = 1, file_name = "inertia_estimation.pkl")
    analyse_data(file_name = "inertia_estimation.pkl")
        
        