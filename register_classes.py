#####################################################################
#                                                                   #
# /labscript_devices/Picomotor8742/register_classes.py                 #
#                                                                   #
# Copyright 2021, Philip Starkey; Edited by Oliver Tu               #
#                                                                   #
# This file is part of labscript_devices, in the labscript suite    #
# (see http://labscriptsuite.org), and is licensed under the        #
# Simplified BSD License. See the license.txt file in the root of   #
# the project for the full license.                                 #
#                                                                   #
#####################################################################
import labscript_devices

#labscript_device_name = 'user_devices.TCPDH_Synth.labscript_devices.TCPDH_Synth'
blacs_tab = 'labscript_devices.Picomotor8742.blacs_tabs.Picomotor8742Tab'
# parser = 'labscript_devices.TCPDH_Synth.runviewer_parsers.TCPDH_SynthTab'

labscript_devices.register_classes(
#    labscript_device_name=labscript_device_name,
    labscript_device_name='Picomotor8742',
    BLACS_tab=blacs_tab,
    runviewer_parser=None,
)

labscript_devices.register_classes(
#    labscript_device_name=labscript_device_name,
    labscript_device_name='TwoPicomotor8081',
    BLACS_tab='labscript_devices.Picomotor8742.blacs_tabs.TwoPicomotor8081Tab',
    runviewer_parser=None,
)