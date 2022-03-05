# from helpplot import HelpPlot
from board01_etherent_connection import HelpEthernetConnection

MY_IP_ADDRESS = '10.0.0.53'
BOARD_01_IP_ADDRESS = '10.0.0.45'


hEC = HelpEthernetConnection(MY_IP_ADDRESS)

some_data = hEC.get_structured_data(5000)


# hP  = HelpPlot(some_data[0]['POSITION']['samples'], some_data[0]['POSITION']['values'], row = 1,col = 1)
# hP2 = HelpPlot(some_data[0]['POSITION']['samples'], some_data[1]['POSITION']['values'], row = 2,col = 1)

# hP3 = HelpPlot(some_data[0]['TORQUE']['samples'], some_data[1]['TORQUE']['values'],
#                subplot= hP.subplot,
#                curve=hP.curve
#                )

# pg.exec()

data_structure_format = 'BHf'
send_data_tuple = (0, 20, 0.2)


__, address_list = hEC.get_raw_data(1)

print(address_list)

hEC.send_structured_data(send_data_tuple, data_structure_format)