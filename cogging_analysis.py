import pickle
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np

data = pickle.load(open("cogging_data_2000pts.pkl",'rb'))



input_positions = np.array(data['input_positions'])
output_positions = np.array(data['output_positions'])
output_torques = np.array(data['output_torques'])

_inds = np.argsort(output_positions)

output_positions = np.take_along_axis(output_positions,_inds, axis = 0)
output_torques  = np.take_along_axis(output_torques,_inds, axis = 0)
input_positions = np.take_along_axis(input_positions,_inds, axis = 0)


points = np.linspace(0,1,1024);
output_torques_interp = np.interp(points, output_positions, output_torques)
b, a = signal.butter(3, 0.4)
output_torques_filtered = signal.filtfilt(b, a, output_torques_interp)

pickle.dump(output_torques_filtered, open("cogging_torque_compensation_values.pkl",'wb'))

# print(output_torques_filtered)


# plt.plot(output_positions, output_torques,'b')
# plt.plot(points, output_torques_interp, 'g')
# plt.plot(points, output_torques_filtered, 'r')

# plt.show()


