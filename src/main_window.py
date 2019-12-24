# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\main_window.ui'
#
# Created: Sun Dec 22 14:43:02 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(787, 690)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 751, 541))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_listen = QtGui.QPushButton(self.gridLayoutWidget)
        self.btn_listen.setObjectName("btn_listen")
        self.verticalLayout.addWidget(self.btn_listen)
        self.btn_close_conn = QtGui.QPushButton(self.gridLayoutWidget)
        self.btn_close_conn.setObjectName("btn_close_conn")
        self.verticalLayout.addWidget(self.btn_close_conn)
        self.btn_send_msg = QtGui.QPushButton(self.gridLayoutWidget)
        self.btn_send_msg.setObjectName("btn_send_msg")
        self.verticalLayout.addWidget(self.btn_send_msg)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.Qlist_conn = QtGui.QListWidget(self.gridLayoutWidget)
        self.Qlist_conn.setObjectName("Qlist_conn")
        self.gridLayout.addWidget(self.Qlist_conn, 0, 0, 1, 1)
        self.Tx_recv = QtGui.QTextEdit(self.gridLayoutWidget)
        self.Tx_recv.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"font: 8pt \"MS Shell Dlg 2\";\n"
"color: green;")
        self.Tx_recv.setReadOnly(False)
        self.Tx_recv.setTabStopWidth(80)
        self.Tx_recv.setAcceptRichText(False)
        self.Tx_recv.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextEditable|QtCore.Qt.TextSelectableByMouse)
        self.Tx_recv.setObjectName("Tx_recv")
        self.gridLayout.addWidget(self.Tx_recv, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 787, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.btn_listen, QtCore.SIGNAL("clicked()"), MainWindow.toggle_listen)
        QtCore.QObject.connect(self.btn_close_conn, QtCore.SIGNAL("clicked()"), MainWindow.close_conn)
        QtCore.QObject.connect(self.btn_send_msg, QtCore.SIGNAL("clicked()"), MainWindow.send_msg)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_listen.setText(QtGui.QApplication.translate("MainWindow", "Listen", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_close_conn.setText(QtGui.QApplication.translate("MainWindow", "Close Connection", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_send_msg.setText(QtGui.QApplication.translate("MainWindow", "send message", None, QtGui.QApplication.UnicodeUTF8))
        self.Tx_recv.setHtml(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

