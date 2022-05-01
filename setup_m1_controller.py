from unicodedata import name
from matplotlib.pyplot import pause
import pyqtgraph as pg
from helpplot import HelpPlot
from board01_etherent_connection import *
import control



def setup_m1_motor(hEC, axis = 1):
    ##########################################################################################
    ### Setting up Velocity estimate filter ##################################################
    K = 100
    tf_pos = control.tf([K],[1,K]);
    tf_pos_disc = control.sample_system(tf_pos, 0.001, method='bilinear');
    tf_vel = control.tf([K, 0],[1,K]);
    tf_vel_disc = control.sample_system(tf_vel, 0.001, method='bilinear');

    hEC.send_parameter(axis, PARAMETER_CLEAR,0, 0);
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

    ##########################################################################################
    ### Setting up Controller gains ##########################################################


    hEC.send_parameter(axis, PARAMETER_CLEAR,0, 0);
    hEC.send_parameter(axis, PARAMETER_TORQUE_CLAMP,0, 3.0)
    hEC.send_parameter(axis, PARAMETER_VELOCITY_LIMIT,0, 5)
    hEC.send_parameter(axis, PARAMETER_VELOCITY_DEADBAND,0, 0.02)

    hEC.send_parameter(axis, PARAMETER_FRICTION_DITHER_RATE,0, 0)
    hEC.send_parameter(axis, PARAMETER_FRICTION_FF_STATIC,0, 0)
    hEC.send_parameter(axis, PARAMETER_FRICTION_FF_KINETIC,0, 0)

    hEC.send_parameter(axis, PARAMETER_POSITION_GAIN,0, 30)
    hEC.send_parameter(axis, PARAMETER_INTEGRATOR_GAIN,0, 1)
    hEC.send_parameter(axis, PARAMETER_INTEGRATOR_CLAMP,0, 3)
    hEC.send_parameter(axis, PARAMETER_DAMPING,0, 10)

    hEC.send_parameter(axis, PARAMETER_COMMIT,0, 0);





if __name__ == "__main__":
    MY_IP_ADDRESS = '10.0.0.53'
    BOARD_01_IP_ADDRESS = '10.0.0.45'
    axis = 1
    hEC = HelpEthernetConnection(MY_IP_ADDRESS)
    setup_m1_motor(hEC, axis = axis)

    hEC.send_parameter(axis, PARAMETER_CLEAR,0, 0);
    hEC.send_parameter(axis, PARAMETER_INPUT_SETPOINT,0, 0.0505)
    hEC.send_parameter(axis, PARAMETER_CONTROLLER_MODE,0, MODE_POSITION_CONSTANT)
