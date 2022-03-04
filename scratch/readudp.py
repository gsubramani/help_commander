
from distutils import command
import socket
import struct
import select

from time import sleep

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from time import perf_counter


win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('pyqtgraph example: Scrolling Plots')

p1 = win.addPlot()
p2 = win.addPlot()
# p3 = win.addPlot()
# p4 = win.addPlot()


position_axis0 = np.zeros(1000);
position_axis1 = np.zeros(1000);

torque_axis0 = np.zeros(1000);
torque_axis1 = np.zeros(1000);



pos1 = p1.plot(position_axis0)

pos2 = p2.plot(position_axis1)
# command2 = p2.plot(position_axis1)


# tor3 = p1.plot(torque_axis0)
# tor4 = p2.plot(torque_axis1)






localIP     = "10.0.0.53"
localPort   = 8888
bufferSize  = 64

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# UDPServerSocket.setblocking(False)

# polling_object = select.poll()
# polling_object.register(UDPServerSocket)
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")
# Listen for incoming datagrams

bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

message = bytesAddressPair[0]
address = bytesAddressPair[1]

clientMsg = "Message from Client:{}".format(message)
clientIP  = "Client IP Address:{}".format(address)
print(clientMsg, ', ', clientIP)

ptr0 = 0
ptr1 = 0
ptr2 = 0
ptr3 = 0



def update():
    global UDPServerSocket, position_axis0, position_axis1, torque_axis0, torque_axis1, ptr0, ptr1, ptr2, ptr3,pos1, pos2 #,tor3,tor4

    pos1.setData(position_axis0)
    
    # command2.setData(position_axis0)
    pos2.setData(position_axis1)
    # tor3.setData(torque_axis0)
    # tor4.setData(torque_axis1)
    
    for i in range(100):

        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        (axis, token_type, data, sample) = struct.unpack('BBfQ',message)
        
        plot_data = {}
        plot_data['axis'] = axis;
        plot_data['token_type'] = token_type;
        plot_data['data'] = data;
        plot_data['sample'] = sample;
        
        if(plot_data['token_type'] == 0):
            
            if(plot_data['axis'] == 0):
                position_axis0[-1] = plot_data['data']
                position_axis0 = np.roll(position_axis0,-1);
                pos1.setPos(ptr0, 0)
                # command2.setPOs(ptr0,0)
                ptr0 += 1

            else:
                position_axis1[-1] = plot_data['data']
                position_axis1 = np.roll(position_axis1,-1);
                pos2.setPos(ptr1, 0)
                ptr1 += 1

        # if(plot_data['token_type'] == 2):
            
        #     if(plot_data['axis'] == 0):
        #         torque_axis0[-1] = plot_data['data']
        #         torque_axis0 = np.roll(torque_axis0,-1);
        #         tor3.setPos(ptr2, 0)
        #         ptr2 += 1

        #     else:
        #         torque_axis1[-1] = plot_data['data']
        #         torque_axis1 = np.roll(torque_axis1,-1);
        #         tor4.setPos(ptr3, 0)
        #         ptr3 += 1

    
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1)

pg.exec()
