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

import control

K = 100


tf_pos = control.tf([K],[1,K]);
tf_pos_disc = control.sample_system(tf_pos, 0.001, method='bilinear');

print("Position TF")
print(tf_pos_disc.num, tf_pos_disc.den)

tf_vel = control.tf([K, 0],[1,K]);
tf_vel_disc = control.sample_system(tf_vel, 0.001, method='bilinear');

print("Velocity TF")
print(tf_vel_disc.num, tf_vel_disc.den)

tf_acc = control.tf([K,0,0],[1,0,K]);
tf_acc_disc = control.sample_system(tf_acc, 0.001, method='bilinear');

print("Acceleration TF")
print(tf_acc_disc.num, tf_acc_disc.den)



MY_IP_ADDRESS = '10.0.0.53'
BOARD_01_IP_ADDRESS = '10.0.0.45'

hEC = HelpEthernetConnection(MY_IP_ADDRESS)



def get_estimates():
    global hEC
    hEC.append_request_data(1, STATE_POSITION)
    hEC.append_request_data(1, STATE_POSITION_ESTIMATE)
    hEC.append_request_data(1, STATE_VELOCITY)
    hEC.append_request_data(1, STATE_VELOCITY_ESTIMATE)
    result = hEC.get_data_request()
    pos = result['response_data'][0]
    pos_est = result['response_data'][1]
    vel = result['response_data'][2]
    vel_est = result['response_data'][3]
    return (pos,pos_est,vel,vel_est)



axis = 1
hEC.send_parameter(axis, PARAMETER_CLEAR,0, 0)
hEC.send_parameter(axis, PARAMETER_CONTROLLER_ACTION,0, ACTION_SET_POSITION_FILTER)

hEC.send_parameter(axis, PARAMETER_POSITION_FILTER_NUM_COEF ,0, tf_pos_disc.num[0][0][0])
hEC.send_parameter(axis, PARAMETER_POSITION_FILTER_NUM_COEF ,1, tf_pos_disc.num[0][0][1])

hEC.send_parameter(axis, PARAMETER_POSITION_FILTER_DEN_COEF ,0, tf_pos_disc.den[0][0][0])
hEC.send_parameter(axis, PARAMETER_POSITION_FILTER_DEN_COEF ,1, tf_pos_disc.den[0][0][1])

hEC.send_parameter(axis, PARAMETER_VELOCITY_FILTER_NUM_COEF ,0, tf_vel_disc.num[0][0][0])
hEC.send_parameter(axis, PARAMETER_VELOCITY_FILTER_NUM_COEF ,1, tf_vel_disc.num[0][0][1])

hEC.send_parameter(axis, PARAMETER_VELOCITY_FILTER_DEN_COEF ,0, tf_vel_disc.den[0][0][0])
hEC.send_parameter(axis, PARAMETER_VELOCITY_FILTER_DEN_COEF ,1, tf_vel_disc.den[0][0][1])


hEC.send_parameter(axis, PARAMETER_COMMIT,0, 0)


poss = []
pos_ests = []

vels = []
vel_ests = []

for i in range(100):
    pos, pos_est, vel, vel_est = get_estimates()
    poss.append(pos)
    pos_ests.append(pos_est)
    vels.append(vel)
    vel_ests.append(vel_est)


plt.subplot(2,1,1)
plt.plot(poss,'r')
plt.plot(pos_ests,'g')

plt.subplot(2,1,2)
plt.plot(vels,'r')
plt.plot(vel_ests,'g')


plt.show()