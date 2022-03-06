import socket
import struct

token_dict = {
                0  : 'POSITION',
                1  : 'VELOCITY',
                2  : 'TORQUE'
}


class HelpEthernetConnection:
    def __init__(self, ip_address_host_):
        self.ip_address_host = ip_address_host_
        
        self.localPort = 8888
        self.bufferSize = 64

        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.bind((self.ip_address_host, self.localPort))

        print("UDP server up and listening")
        bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)

        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        clientMsg = "Message from Client:{}".format(message)
        clientIP = "Client IP Address:{}".format(address)
        
        self.address_board01 = address
        
        print(clientMsg, ', ', clientIP)

        print("Connection Established")

    def send_raw_data(self, data):
        self.UDPServerSocket.sendto(data, self.address_board01)

    def send_structured_data(self, data_tuple, structure):
        data = struct.pack(structure, *data_tuple)
        self.send_raw_data(data)

    def send_parameter(self, axis, param, value):
        data_structure_format = 'BHf'
        send_data_tuple = (axis, param,value)
        self.send_structured_data(send_data_tuple, data_structure_format)

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
