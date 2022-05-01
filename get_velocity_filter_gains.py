import control
import matplotlib.pyplot as plt


K = 10

tf_vel = control.tf([K],[1,K]);
tf_vel_disc = control.sample_system(tf_vel, 0.001, method='bilinear');

mag, phase, omega = control.bode(tf_vel_disc)

plt.show()


print(tf_vel_disc.num[0][0][0], tf_vel_disc.den)
