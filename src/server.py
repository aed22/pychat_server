import socket
import threading
import sys
import time
# import Queue

class server():
    
    def __init__(self, 
                name= "serv", 
                port= 5678,
                connect=None,
                data_recd = None,
                ):
        
        self._connect = connect
        self._data_recd = data_recd


        ip = socket.gethostbyname(socket.gethostname())
        self.addr = {}
        self.addr['ip'] = ip
        self.addr['port'] = port
        self.conn_list = []
        

        self.lthread = threading.Thread(target=self.listen, daemon=True)
        self.conn_hndls_threads = []
        
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("socket is created")
        
        self.lsock.bind((ip, port))
        print("socket is bound to ip:{}| port:{}".format(ip, port))
        

    def __del__(self):
        print("socket destructor called")
        try:
            for c in self.conn_list:
                c.close()
            self.s.close()
        except:
            pass
    
    def listen(self):
        print("enter listen")
        
        self.lsock.listen(5)

        while True:
            conn, addr = self.lsock.accept()
            print("listening")
            self.conn_list.append(conn)
            handle_thread = threading.Thread(target=self.handle_conn, args=(conn, addr), daemon=True )
            self.conn_hndls_threads.append(handle_thread)
            handle_thread.start()
            
        pass


    def start_server(self):
        print("start server")
        self.lthread.start()
        pass
        
    def handle_conn(self, conn:socket.socket, addr):
        print("connection recieved from {}".format(addr) )
        
        try:
            self._connect.emit({addr})
        except:
            pass

        text = ''
        while True:
            data = conn.recv(1024)
            if not data:
                print("connection closed")
                conn.close()
                break
            text += data.decode()
            self._data_recd.emit({data.decode()})
            print("{}:{}".format(addr, data))    
        print("#####################################")
        print(text)

    


if __name__ == "__main__":
    s = server()
    s.listen()