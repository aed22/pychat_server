from PySide import QtCore as core
from PySide import QtGui as gui
import server
from PySide.QtCore import QThread


class serv_interface(QThread):
    connect_signal = core.Signal(dict)
    data_signal = core.Signal(dict)
    

    def __init__(self,
                connect_callback,
                recvd_data):
        
        super(serv_interface, self).__init__()

        self.connect_signal.connect(connect_callback)
        self.data_signal.connect(recvd_data)
        self.server_obj = server.server(    connect=self.connect_signal,
                                            data_recd=self.data_signal)

    
    def run(self):
        # self.start_listen()
        # while True:
        #     pass
        print("interface running")
        
    def start_listen(self, max_conn):
        self.server_obj.start_server()
    

    def close_conn(self):
        pass

    def send_mesg(self):
        pass
    
