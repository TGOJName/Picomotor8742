#####################################################################
#                                                                   #
# /labscript_devices/Picomotor8742/blacs_worker.py                       #
#                                                                   #
# This file is part of labscript_devices                            #
#                                                                   #
#####################################################################
from asyncio.log import logger
import logging
from formatter import NullFormatter
import labscript_utils.h5_lock
import h5py
from blacs.tab_base_classes import Worker
from labscript_utils.connections import _ensure_str
import labscript_utils.properties as properties
from time import sleep
from threading import Thread

class Picomotor8742Worker(Worker):
    def init(self):
        # logging.basicConfig(level=logging.DEBUG) # Use this line to debugging 
        global socket; import socket
        global h5py; import labscript_utils.h5_lock, h5py 
        self.server_address = (self.TCPIP_address,23)
        self.check_remote_values(True)

    


    def sendinstr(self,instr,respond = False,motion = False, show=True):
        clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            clientsock.connect(self.server_address)
            clientsock.recv(4096) # The picomotor will return a dummy code when connected successfully
        except ConnectionRefusedError as msg:
            self.logger.debug(f"ConnectionRefusedError: server {self.server_address} is most likely down.")
            raise
        clientsock.sendall((instr+'\r').encode())
        if respond:
            response = clientsock.recv(4096).decode()
            if show:
                print("Response of "+instr+": "+response)
        elif motion:
            while True:
                checker='%uMD?\r'%int(instr[0])
                clientsock.send(checker.encode())
                if int(clientsock.recv(1024).decode()):
                    break
                else:
                    sleep(0.1)
        clientsock.close()
        if respond:
            return response
   
    def check_remote_values(self,inital = False):
        results = {}
        if inital:
            self.current_position = [0,0,0,0]
        for i in range(4):
            command = '%uTP?'%(i+1)
            self.current_position[i] = int(self.sendinstr(command,respond=True,show=False))
            results["motor#%u position"%(i+1)]=self.current_position[i]
        return results

    def program_manual(self,front_panel_values):
        fp_values = [front_panel_values['motor#1 position'],front_panel_values['motor#2 position'],front_panel_values['motor#3 position'],front_panel_values['motor#4 position']]
        for i in range(4):
            if fp_values[i] != self.current_position[i]:
                command = '%uPA%u'%(i+1,fp_values[i])
                self.sendinstr(command,motion=True)
                self.current_position[i] = fp_values[i]
        return front_panel_values
    
    def threaded_worker(self,worklist,address):
        for command in worklist:
            clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                clientsock.connect(address)
                clientsock.recv(4096)
            except ConnectionRefusedError as msg:
                raise
            command += '\r'
            clientsock.sendall(command.encode())
            while True:
                checker='%uMD?\r'%int(command[0])
                clientsock.send(checker.encode())
                if int(clientsock.recv(1024).decode()):
                    break
                else:
                    sleep(0.1)   
            clientsock.close() 

    def transition_to_buffered(self,device_name,h5file,initial_values,fresh):
        final_values = {}
        worklist = []
        with h5py.File(h5file, 'r') as hdf5_file:
            group = hdf5_file['/devices/'+device_name]
            tabledata = group['DATA']
            for i in range(4):
                if self.current_position[i] != tabledata['motor%u'%(i+1)]:
                    command = '%uPA%u'%(i+1,tabledata['motor%u'%(i+1)])
                    worklist.append(command)
                    self.current_position[i] = tabledata['motor%u'%(i+1)]
                    final_values['motor#%u position'%(i+1)] = self.current_position[i]
            self.thread = Thread(target = self.threaded_worker, args = (worklist,self.server_address))
            self.thread.start()
        return final_values
    
    def abort_transition_to_buffered(self):
        self.sendinstr('ST')
        return self.transition_to_manual(True)
        
    def abort_buffered(self):
        self.sendinstr('ST')
        return self.transition_to_manual(True)
    
    def transition_to_manual(self,abort = False):
        try:
            self.thread.join()
        except:
            pass
        if abort:
            self.sendinstr('ST')
        return True

    def shutdown(self):
        self.sendinstr('ST')


class TwoPicomotor8081Worker(Worker):
    def init(self):
        # logging.basicConfig(level=logging.DEBUG) # Use this line to debugging 
        global socket; import socket
        global h5py; import labscript_utils.h5_lock, h5py 
        self.server_address = [(self.TCPIP_address1,23),(self.TCPIP_address2,23),(self.TCPIP_address3,23)]
        self.name_dict=[["1A","1B","1A'","1B'"],["2A","2B","2A'","2B'"],["1C","2C"]]
        self.check_remote_values(True)
        
        
    def instrsender(self, instr,driver,respond, motion, show):
        clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            clientsock.connect(self.server_address[driver])
            clientsock.recv(4096) # The picomotor will return a dummy code when connected successfully
        except ConnectionRefusedError as msg:
            self.logger.debug(f"ConnectionRefusedError: server {self.server_address} is most likely down.")
            raise
        clientsock.sendall((instr+'\r').encode())
        if respond:
            response = clientsock.recv(4096).decode()
            if show:
                print("Response of "+instr+": "+response)
        elif motion:
            while True:
                checker='%uMD?\r'%int(instr[0])
                clientsock.send(checker.encode())
                if int(clientsock.recv(1024).decode()):
                    break
                else:
                    sleep(0.1)
        clientsock.close()
        if respond:
            return response
   
    def sendinstr(self, instr, respond=False, motion=False, show=True,driver=-1):
        if driver == -1:
            for i in range(3):
                self.instrsender(instr,i,respond, motion, show)
        else:
            return self.instrsender(instr,driver,respond, motion, show)

    def check_remote_values(self,inital = False):
        results = {}
        if inital:
            self.current_position = [[0,0,0,0],[0,0,0,0],[0,0]]
        for j in range(3):
            for i in range(len(self.current_position[j])):
                command = '%uTP?'%(i+1)
                self.current_position[j][i] = int(self.sendinstr(command,driver=j,respond=True,show=False))
                results["motor %s position"%(self.name_dict[j][i])]=self.current_position[j][i]
        return results

    def program_manual(self,front_panel_values):
        fp_values=[[[],[],[],[]],[[],[],[],[]],[[],[]]]
        for j in range(3):
            for i in range(len(fp_values[j])):
                fp_values[j][i]=front_panel_values["motor %s position"%(self.name_dict[j][i])]
                if fp_values[j][i] != self.current_position[j][i]:
                    command = '%uPA%u'%(i+1,fp_values[j][i])
                    print(command)
                    self.sendinstr(command, driver=j, motion=True)
                    self.current_position[j][i] = fp_values[j][i]
        return front_panel_values
    
    def threaded_worker(self,worklist,ip_dict):
        for pair in worklist:
            clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                clientsock.connect(ip_dict[pair[0]])
                clientsock.recv(4096)
            except ConnectionRefusedError as msg:
                raise
            tcommand = pair[1]+'\r'
            clientsock.sendall(tcommand.encode())
            while True:
                checker='%uMD?\r'%int(pair[1][0])
                clientsock.send(checker.encode())
                if int(clientsock.recv(1024).decode()):
                    break
                else:
                    sleep(0.1)   
            clientsock.close()         

    def transition_to_buffered(self,device_name,h5file,initial_values,fresh):
        final_values = {}
        worklist=[]
        with h5py.File(h5file, 'r') as hdf5_file:
            group = hdf5_file['/devices/'+device_name]
            tabledata = [group['D1'],group['D2'],group['D3']]
            for j in range(3):
                for i in range(len(self.name_dict[j])):
                    print(tabledata[0][0][0])
                    if self.current_position[j][i] != tabledata[j][0][i]:
                        command = '%uPA%u'%(i+1,tabledata[j][0][i])
                        worklist.append((j,command))
                         #TODO: Threading here
                        self.current_position[j][i] = tabledata[j][0][i]
                        final_values["motor %s position"%(self.name_dict[j][i])] = self.current_position[j][i]
            self.thread = Thread(target = self.threaded_worker, args = (worklist, self.server_address))
            self.thread.start()
        return final_values
    
    def abort_transition_to_buffered(self):
        self.sendinstr('ST')
        return self.transition_to_manual(True)
        
    def abort_buffered(self):
        self.sendinstr('ST')
        return self.transition_to_manual(True)
    
    def transition_to_manual(self,abort = False):
        try:
            self.thread.join()
        except:
            pass
        if abort:
            self.sendinstr('ST')
        return True

    def shutdown(self):
        self.sendinstr('ST')

     
