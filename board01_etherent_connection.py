import socket
import struct

token_dict = {
                0  : 'POSITION',
                1  : 'VELOCITY',
                2  : 'TORQUE'
}

# parameters
PARAMETER_CLEAR = 0
PARAMETER_COMMIT = 1

PARAMETER_POSITION_GAIN = 10 
PARAMETER_VELOCITY_GAIN = 11
PARAMETER_INTEGRATOR_GAIN = 12

PARAMETER_INTEGRATOR_CLAMP = 13
PARAMETER_TORQUE_CLAMP = 14
PARAMETER_INPUT_SETPOINT = 15

PARAMETER_DAMPING = 16
PARAMETER_VELOCITY_DEADBAND = 17

PARAMETER_FRICTION_FF_STATIC = 18
PARAMETER_FRICTION_DITHER_RATE = 19
PARAMETER_FRICTION_DITHER_BAND = 20
PARAMETER_FRICTION_FF_KINETIC = 21


PARAMETER_CONTROLLER_MODE = 25
PARAMETER_INPUT_AMPLITUDE = 26
PARAMETER_INPUT_FREQUENCY = 27
PARAMETER_VELOCITY_LIMIT = 28    


STATE_POSITION   = 101
STATE_VELOCITY   = 102
STATE_TORQUE     = 103

# modes
MODE_IDLE                    = 0

MODE_TORQUE_SIN_TRAJECTORY   = 1
MODE_TORQUE_CONSTANT         = 2
MODE_TORQUE_RAMP             = 3

MODE_POSITION_SIN_TRAJECTORY = 11
MODE_POSITION_CONSTANT       = 12
MODE_POSITION_RAMP           = 13

CSTRING_TOKEN_SIZE = 32
MAX_NUM_REQUEST_STATES =  32

MAX_GENERAL_DATA_PACKET_PAYLOAD = 256

GET_STATES_REQUEST = b"GET_STATES_REQUEST";

GET_STATES_RESPONSE = b"GET_STATES_RESPONSE";              
GET_STATES_RESPONSE_STRUCTURE = 'IL' + MAX_NUM_REQUEST_STATES*'f'            

SET_PARAMETER = b"SET_PARAMETER";

PUBLISHER = b"PUBLISHER"
PUBLISHER_RESPONSE_STRUCTURE = 'BBfq'

PARAMETER_HEADER_STRUCTURE =    str(CSTRING_TOKEN_SIZE) + 's'  \
                              + str(CSTRING_TOKEN_SIZE) + 's'  \
                              + str(CSTRING_TOKEN_SIZE) + 's'  \
                              + 'I'
                              
GENERAL_DATA_PACKET_STRUCTURE = PARAMETER_HEADER_STRUCTURE \
                              + str(MAX_GENERAL_DATA_PACKET_PAYLOAD) + 's'


                              
class HelpEthernetConnection:
    
    def __init__(self, ip_address_host_):
        self.ip_address_host = ip_address_host_
        
        self.localPort = 8888
        self.bufferSize = 400

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
        
        self.num_parameter_updates = 0
        
        self.request_id = 0        
        self.reset_data_request()

    def reset_data_request(self):
        self.data_request = {}
        self.data_request["data_request_index"] = 0
        self.data_request['axis'] = MAX_NUM_REQUEST_STATES*[0]
        self.data_request['param'] = MAX_NUM_REQUEST_STATES*[0]
    

    def send_raw_data(self, data):
        self.UDPServerSocket.sendto(data, self.address_board01)

    def send_structured_data(self, data_tuple, structure):
        data = struct.pack(structure, *data_tuple)
        self.send_raw_data(data)

    def append_request_data(self, axis, param):
        self.data_request['axis'][self.data_request["data_request_index"]] = axis
        self.data_request['param'][self.data_request["data_request_index"]] = param
        self.data_request["data_request_index"] +=1

    def push_data_request(self):
        num_requests = len(self.data_request['axis'])
        
        data_structure_format = 'I' # request id
        data_structure_format += 'I' # num requested states
        data_structure_format += 'B'*MAX_NUM_REQUEST_STATES # axis
        data_structure_format += 'H'*MAX_NUM_REQUEST_STATES # parameter_lookup 
        
        size_of_parameter_update_packet = struct.calcsize(data_structure_format)

        send_data_tuple = (GET_STATES_REQUEST ,
                           b'computer',
                           b'teensy',
                           size_of_parameter_update_packet, 
                           self.request_id, 
                           num_requests , 
                           *tuple(self.data_request['axis']), 
                           *tuple(self.data_request['param']))

        print(struct.calcsize(PARAMETER_HEADER_STRUCTURE + data_structure_format))
                
        self.send_structured_data(send_data_tuple, PARAMETER_HEADER_STRUCTURE + data_structure_format)
        


    def send_parameter(self, axis, param, value):
        
        self.num_parameter_updates += 1;
        
        if param == PARAMETER_COMMIT:
            data_structure_format = 'BHI'
            value = self.num_parameter_updates;
            print(value)
            self.num_parameter_updates = 0;
            
        elif param == PARAMETER_CLEAR:
            data_structure_format = 'BHI'
            self.num_parameter_updates = 0;
        
        elif param == PARAMETER_CONTROLLER_MODE:
            data_structure_format = 'BHI'
        
        else:    
            data_structure_format = 'BHf'
        
        size_of_parameter_update_packet = struct.calcsize(data_structure_format)
            
        send_data_tuple = (SET_PARAMETER ,b'computer' ,b'teensy', size_of_parameter_update_packet, axis, param, value)
        self.send_structured_data(send_data_tuple, PARAMETER_HEADER_STRUCTURE + data_structure_format)

    def get_raw_data(self, num_packets):
        messages = []
        addresses = []
        for ii in range(num_packets):
            self.bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)
            messages.append(self.bytesAddressPair[0])
            addresses.append(self.bytesAddressPair[1])
        return messages, addresses

    def parse_udp_data_from_rv1core(self):
        # get the header first
        
        self.bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)
        # print(self.bytesAddressPair)
        message = self.bytesAddressPair[0]
        if(len(message) < struct.calcsize(PARAMETER_HEADER_STRUCTURE)):
            return

        (name, source, destination, data_packet_size) = struct.unpack(PARAMETER_HEADER_STRUCTURE, message[:struct.calcsize(PARAMETER_HEADER_STRUCTURE)])
        
        payload = message[struct.calcsize(PARAMETER_HEADER_STRUCTURE): struct.calcsize(PARAMETER_HEADER_STRUCTURE) + data_packet_size]

        if(GET_STATES_RESPONSE == name[:len(GET_STATES_RESPONSE)]):
            
            unpacked_data = struct.unpack(GET_STATES_RESPONSE_STRUCTURE, payload)
            
            request_id = unpacked_data[0];
            time_stamp = unpacked_data[1];
            response_data = unpacked_data[2:];
            print (request_id,time_stamp, response_data)

        if(PUBLISHER  == name[:len(PUBLISHER)]):   
            unpacked_data = struct.unpack(PUBLISHER_RESPONSE_STRUCTURE, payload)
                        
            axis = unpacked_data[0];
            token_type = unpacked_data[1];
            data = unpacked_data[2];
            sample = unpacked_data[3];
            
            print (axis,token_type, data, sample)
            


    def tag_messages(self, messages):
        pass

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
