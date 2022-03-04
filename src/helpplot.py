import socket
import struct
from time import sleep

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from time import perf_counter
import numpy as np


MY_IP_ADDRESS = '10.0.0.200'

token_dict = {
                0 : 'POSITION',
                2 : 'TORQUE'
}


class HelpEthernetConnection:
    def __init__(self, ip_address_):
        self.ip_address = ip_address_
        self.localPort = 8888
        self.bufferSize = 64

        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.bind((self.ip_address, self.localPort))

        print("UDP server up and listening")
        bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)

        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        clientMsg = "Message from Client:{}".format(message)
        clientIP = "Client IP Address:{}".format(address)
        print(clientMsg, ', ', clientIP)

        print("Connection Established")

    def get_raw_data(self, num_packets):
        messages = []
        addresses = []
        for ii in range(num_packets):
            self.bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)
            messages.append(self.bytesAddressPair[0])
            addresses.append(self.bytesAddressPair[1])
        return messages, addresses

    def get_structured_data(self, num_packets, structure = 'BBfQ'):

        (messages, _) = self.get_raw_data(num_packets)

        plot_data_list = []
        plot_data_struct = {}

        axes = []
        token_types = []

        for message in messages:
            (axis, token_type, data, sample) = struct.unpack(structure, message)
            plot_data = {}
            plot_data['axis'] = axis
            plot_data['token_type'] = token_type
            plot_data['data'] = data
            plot_data['sample'] = sample
            plot_data_list.append(plot_data)
            axes.append(axis)
            token_types.append(token_type)

        axes = set(axes)
        token_types = set(token_types)

        for axis in axes:
            plot_data_struct[axis] = {}

        for axis in axes:
            for token_type in token_types:
                plot_data_struct[axis][token_dict[token_type]] = {
                    'samples' : [],
                    'values' : []
                }

        print('Structure of data is: ', plot_data_struct)


        for plot_data in plot_data_list:

            axis = plot_data['axis']
            token_name = token_dict[plot_data['token_type']]

            plot_data_struct[axis][token_name]['samples'].append(plot_data['sample'])
            plot_data_struct[axis][token_name]['values'].append(plot_data['data'])

        return plot_data_struct


class HelpPlot:

    win = pg.GraphicsLayoutWidget(show=True)
    win.setWindowTitle('Help Plots')

    def __init__(self, x, y, curve = None, subplot = None, row = None, col = None, pen = pg.mkPen('b', width=2)):

        if(subplot is None):
            if(row == None or col == None):
                self.subplot = self.win.addPlot()
            else:
                self.subplot = self.win.addPlot(row=row, col=col)
            self.curve = self.subplot.plot(x, y, pen = pen)
            return

        else:
            self.subplot = subplot

        if(curve is None):
            self.curve = self.subplot.plot(x, y, pen = pen)
        else:
            self.subplot.plot(x,y, pen = pen)
        return




hEC = HelpEthernetConnection(MY_IP_ADDRESS)

some_data = hEC.get_structured_data(5000)


hP  = HelpPlot(some_data[0]['POSITION']['samples'], some_data[0]['POSITION']['values'], row = 1,col = 1)
hP2 = HelpPlot(some_data[0]['POSITION']['samples'], some_data[1]['POSITION']['values'], row = 2,col = 1)

hP3 = HelpPlot(some_data[0]['TORQUE']['samples'], some_data[1]['TORQUE']['values'],
               subplot= hP.subplot,
               curve=hP.curve
               )

pg.exec()

# timer = pg.QtCore.QTimer()
# timer.timeout.connect(update)
# timer.start(1)
#
# pg.exec()
