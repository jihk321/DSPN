# from main import * 
import sys
from counting import *
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QCompleter, QVBoxLayout, QDialog
# from PyQt5.QtCore import Qt
from PyQt5 import uic


class Recommed(QWidget):

    def __init__(self,name):
        super().__init__()

        self.name = name 
        re = FindingClient(self.name)

        self.lineEdit = QLineEdit() #라인 에딧 생성
        
        completer = QCompleter(re)
        self.lineEdit.setCompleter(completer)

        box = QVBoxLayout()
        box.addWidget(self.lineEdit)
        self.setLayout(box)
        self.show()


# form_second = uic.loadUiType("subplan.ui")[0]

# class SubWindow(QDialog,form_second):

#     def __init__(self) :
#         super(SubWindow, self).__init__()
#         self.initUI()

#     def initUI(self) :
#         self.setupUi(self)
#         self.show()
        
# if __name__ == "__main__" :
#     app = QApplication(sys.argv)
#     ss = SubWindow()
#     app.exec_()
