#####################################################################
#                                                                   #
# /labscript_devices/Picomotor8742/labscript_devices.py.py                  #
#                                                                   #
# Copyright 2021, Philip Starkey; Edited by Oliver Tu               #
#                                                                   #
# This file is part of the module labscript_devices, in the         #
# labscript suite (see http://labscriptsuite.org), and is           #
# licensed under the Simplified BSD License. See the license.txt    #
# file in the root of the project for the full license.             #
#                                                                   #
#####################################################################


from labscript_devices import runviewer_parser

from labscript import config, set_passed_properties,IntermediateDevice
import labscript_utils.properties
import numpy as np

__author__ = ['Oliver Tu']

class Picomotor8742(IntermediateDevice):
    """
    This class is initilzed with the key word argument
    'TCPIP_address'  -- 
    """
    description = 'Picomotor8742'
    allowed_children = []

    @set_passed_properties(
        property_names={
            'connection_table_properties': [
                'TCPIP_address',
            ]
        }
    )
    def __init__(
        self,
        name,
        parent_device,
        TCPIP_address='192.168.1.150',
        **kwargs
    ):
        IntermediateDevice.__init__(self, name, parent_device, **kwargs)
        self.BLACS_connection = '%s'%(TCPIP_address)
        self.target_position = [0,0,0,0]

    def move_to(self,t,motor,position):
        if motor != int(motor) or motor > 4 or motor < 1:
            raise ValueError('Motor Index Out of Range')
        elif position != int(position) or position > 2**31 or position < -2**31:
            raise ValueError('Position Out of Range: Should be between +- 2^31')
        else:
            self.target_position[int(motor)-1]=int(position)

    def generate_code(self, hdf5_file):
        dtypes = {'names':['motor1','motor2','motor3','motor4'],'formats':[np.uint32,np.uint32,np.uint32,np.uint32]}

        out_table = np.zeros(1,dtype=dtypes)# create the table data for the hdf5 file.
        out_table['motor1'].fill(self.target_position[0])
        out_table['motor2'].fill(self.target_position[1])
        out_table['motor3'].fill(self.target_position[2])
        out_table['motor4'].fill(self.target_position[3])
        grp = self.init_device_group(hdf5_file)
        grp.create_dataset('DATA',compression=config.compression,data=out_table) 

class TwoPicomotor8081(IntermediateDevice):
    """
    This class is initilzed with the four key word argument
    'TCPIP_address'  -- 

    Besides, the arrangement for the picomotors connection is assigned in the following ways:
        Picomotor driver 8742 (abbreviated as D8742) #1: Motor #1-#4 corresponds the Motor #A, #B, #A', #B' of the first 8081 stage;
        D8742 #2: Motor #1-#4 corresponds the Motor #A, #B, #A', #B' of the second 8081 stage;
        D8742 #3: Motor #1-#2 corresponds the Motor #C of the first and second 8081 stage;
    """
    description = 'TwoPicomotor8081'
    allowed_children = []

    @set_passed_properties(
        property_names={
            'connection_table_properties': [
                'TCPIP_address1',
                'TCPIP_address2',
                'TCPIP_address3',
            ]
        }
    )
    def __init__(
        self,
        name,
        parent_device,
        TCPIP_address1='192.168.1.150',
        TCPIP_address2='192.168.1.151',
        TCPIP_address3='192.168.1.152',
        **kwargs
    ):
        IntermediateDevice.__init__(self, name, parent_device, **kwargs)
        self.BLACS_connection = 'D8742#1:%s, D8742#2:%s, D8742#3:%s'%(TCPIP_address1,TCPIP_address2,TCPIP_address3)
        self.target_position = {'1':[0,0,0,0],'2':[0,0,0,0],'3':[0,0]} # Here the number is the index of the 8742 drivers
        self.index_dict = {"1A":1, "1B": 2, "1A'": 3, "1B'": 4,"2A":1, "2B": 2, "2A'": 3, "2B'": 4, "1C":1,"2C":2}

    def move_to(self,t,motor,position):
        try:
            motor_index = self.index_dict[motor]
        except:
            raise ValueError('Motor Index Incorrect or Out of Range')
        if position != int(position) or position > 2**31 or position < -2**31:
            raise ValueError('Position Out of Range: Should be between +- 2^31')
        else:
            self.target_position[motor[0]][int(motor_index)-1]=int(position)

    def generate_code(self, hdf5_file):
        dtypes = {'names':['motor1','motor2','motor3','motor4'],'formats':[np.uint32,np.uint32,np.uint32,np.uint32]}

        out_table = np.zeros(1,dtype=dtypes)# create the table data for the hdf5 file.
        out_table['motor1'].fill(self.target_position["1"][0])
        out_table['motor2'].fill(self.target_position["1"][1])
        out_table['motor3'].fill(self.target_position["1"][2])
        out_table['motor4'].fill(self.target_position["1"][3])
        grp = self.init_device_group(hdf5_file)
        grp.create_dataset('D1',compression=config.compression,data=out_table) 

        out_table = np.zeros(1,dtype=dtypes)# create the table data for the hdf5 file.
        out_table['motor1'].fill(self.target_position["2"][0])
        out_table['motor2'].fill(self.target_position["2"][1])
        out_table['motor3'].fill(self.target_position["2"][2])
        out_table['motor4'].fill(self.target_position["2"][3])
        grp.create_dataset('D2',compression=config.compression,data=out_table) 

        out_table = np.zeros(1,dtype=dtypes)# create the table data for the hdf5 file.
        out_table['motor1'].fill(self.target_position["3"][0])
        out_table['motor2'].fill(self.target_position["3"][1])
        grp.create_dataset('D3',compression=config.compression,data=out_table) 