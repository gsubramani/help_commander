from board01_etherent_connection import *


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
    