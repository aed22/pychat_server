from main_window import Ui_MainWindow
import PySide.QtCore as core
import PySide.QtGui as gui
import sys
import server_interface


class window(gui.QMainWindow, Ui_MainWindow):
    
    def __init__(self):

        super(window, self).__init__()
        self.setupUi(self)
        self.listening = False

        self.Qlist_conn.addItem("hello there")
        self.update_text("ghsfdn")
        self.show()
        self.interface = server_interface.serv_interface(self.update_list, self.update_text)
        self.interface.start()


    def toggle_listen(self):
        print("toggle listen")
        self.interface.start_listen(5)
        


    def close_conn(self):
        print("close conn")

    def send_msg(self):
        print("send msg")

    def update_text(self, mesg):
        self.Tx_recv.append(str(mesg))

    def update_list(self, attr):
        self.Qlist_conn.addItem(str(attr))

if __name__ == '__main__':
    app = gui.QApplication(sys.argv)
    mainWin = window()
    ret = app.exec_()
    sys.exit( ret ) 
    
