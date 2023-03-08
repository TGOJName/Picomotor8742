#####################################################################
#                                                                   #
# /labscript_devices/Picomotor8742/blacs_tab.py                        #
#                                                                   #
# Copyright 2021, Philip Starkey; edited by Oliver Tu               #
#                                                                   #
# This file is part of labscript_devices, in the labscript suite    #
# (see http://labscriptsuite.org), and is licensed under the        #
# Simplified BSD License. See the license.txt file in the root of   #
# the project for the full license.                                 #
#                                                                   #
#####################################################################
from blacs.device_base_class import (
    DeviceTab,
    define_state,
    MODE_BUFFERED,
    MODE_MANUAL,
    MODE_TRANSITION_TO_BUFFERED,
    MODE_TRANSITION_TO_MANUAL,
)
import labscript_utils.properties
from qtutils.qt import QtWidgets

class Picomotor8742Tab(DeviceTab):
    def initialise_GUI(self):        
        connection_object = self.settings['connection_table'].find_by_name(self.device_name)
        connection_table_properties = connection_object.properties

        picoMotorProp = {}
        for i in range(4):
            picoMotorProp['motor#%d position' % (i+1)] = {
                'base_unit': 'step',
                'min': -2147483648,
                'max': 2147483648,
                'step': 1,
                'decimals': 0,
            }

        # Create DDS Output objects: we only need frequency for the carrier and frequency and phase for the mod
        self.create_analog_outputs(picoMotorProp)

        # Create widgets for outputs defined so far (i.e. analog outputs only)
        _, AO_widgets, _ = self.auto_create_widgets()  
        widget_list = [("Analog outputs", AO_widgets)]
        self.auto_place_widgets(*widget_list)
        # Connect signals for buttons
        # Add icons
        

        
        self.TCPIP_address = connection_table_properties.get('TCPIP_address', None)

        
        # Create and set the primary worker
        self.create_worker("main_worker",
                            'labscript_devices.Picomotor8742.blacs_workers.Picomotor8742Worker',
                            {'TCPIP_address': self.TCPIP_address})
        
        self.primary_worker = "main_worker"

        # Set the capabilities of this device
        self.supports_remote_value_check(True)
        self.supports_smart_programming(False) 


class TwoPicomotor8081Tab(DeviceTab):
    def initialise_GUI(self):        
        connection_object = self.settings['connection_table'].find_by_name(self.device_name)
        connection_table_properties = connection_object.properties

        picoMotorProp = {}
        for i in [1,2]:
            for j in ["A","B","A'","B'","C"]:
                    picoMotorProp["motor %d%s position" % (i,j)] = {
                    'base_unit': 'step',
                    'min': -2147483648,
                    'max': 2147483648,
                    'step': 1,
                    'decimals': 0,
                }

        # Create DDS Output objects: we only need frequency for the carrier and frequency and phase for the mod
        self.create_analog_outputs(picoMotorProp)

        # Create widgets for outputs defined so far (i.e. analog outputs only)
        _, AO_widgets, _ = self.auto_create_widgets()  
        widget_list = [("Analog outputs", AO_widgets)]
        self.auto_place_widgets(*widget_list)
        # Connect signals for buttons
        # Add icons
        

        
        self.TCPIP_address1 = connection_table_properties.get('TCPIP_address1', None)
        self.TCPIP_address2 = connection_table_properties.get('TCPIP_address2', None)
        self.TCPIP_address3 = connection_table_properties.get('TCPIP_address3', None)

        
        # Create and set the primary worker
        self.create_worker("main_worker",
                            'labscript_devices.Picomotor8742.blacs_workers.TwoPicomotor8081Worker',
                            {'TCPIP_address1': self.TCPIP_address1,'TCPIP_address2': self.TCPIP_address2,'TCPIP_address3': self.TCPIP_address3})
        
        self.primary_worker = "main_worker"

        # Set the capabilities of this device
        self.supports_remote_value_check(True)
        self.supports_smart_programming(False) 
