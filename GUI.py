from PyQt4.uic import loadUiType
from PyQt4 import  QtGui ,uic,QtCore
from PyQt4.QtGui import *

#from PySide import  QtGui ,uic,QtCore
#from PySide.QtGui import *

#from PySide import QtCore, QtGui
import sys, os

class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__()
        uic.loadUi(self.resource_path('DIO_config_Tool.ui'), self)
        pixmap = QPixmap("sobhy.jpg")
        self.label_image.setPixmap(pixmap)
        self.label_image.setScaledContents(True)
        self.pushButton_SaveCurrent.clicked.connect(self.SaveCurrentPinsConfigToDict)
        self.pushButton_new.clicked.connect(self.NewPinsConfiguration)
        self.pushButton_load.clicked.connect(self.LoadPinsConfigurationFromFile)
        self.pushButton_save.clicked.connect(self.SavePinsConfigurationToFile)
        self.pushButton_Browse.clicked.connect(self.browse)
        self.pushButton_FinalSave.setStyleSheet("background-color: green")  ## This is to change Button Color
        self.checkboxesPins=[
            self.checkBox_0,self.checkBox_1,self.checkBox_2,self.checkBox_3,self.checkBox_4,self.checkBox_5,self.checkBox_6,self.checkBox_7 ,self.checkBox_8,\
            self.checkBox_9,self.checkBox_10,self.checkBox_11,self.checkBox_12,self.checkBox_13,self.checkBox_14,self.checkBox_15,self.checkBox_16, \
            self.checkBox_17, self.checkBox_18, self.checkBox_19,self.checkBox_20, self.checkBox_21,self.checkBox_22,self.checkBox_23,self.checkBox_24,\
            self.checkBox_25, self.checkBox_26,self.checkBox_27, self.checkBox_28,self.checkBox_29,self.checkBox_30,self.checkBox_31]
        self.labelsPins=[
            self.label_0,self.label_1,self.label_2,self.label_3,self.label_4,self.label_5,self.label_6,self.label_7, \
            self.label_8, self.label_9, self.label_10, self.label_11, self.label_12, self.label_13, self.label_14,self.label_15, \
            self.label_16, self.label_17, self.label_18, self.label_19, self.label_20, self.label_21, self.label_22,self.label_23, \
            self.label_24, self.label_25, self.label_26, self.label_27, self.label_28, self.label_29, self.label_30,self.label_31
            ]
        self.pins_dict_init = {
            "0": "not configured", "1": "not configured", "2": "not configured", "3": "not configured",
            "4": "not configured", "5": "not configured", "6": "not configured", "7": "not configured",
            "8": "not configured", "9": "not configured", "10": "not configured", "11": "not configured",
            "12": "not configured", "13": "not configured", "14": "not configured", "15": "not configured",
            "16": "not configured", "17": "not configured", "18": "not configured", "19": "not configured",
            "20": "not configured", "21": "not configured", "22": "not configured", "23": "not configured",
            "24": "not configured", "25": "not configured", "26": "not configured", "27": "not configured",
            "28": "not configured", "29": "not configured", "30": "not configured", "31": "not configured"
        }
        self.pins_dict =self.pins_dict_init
    def apply_pinsLabels(self):
        for index in range (31):
            state =self.pins_dict[str(index)]
            self.labelsPins[index].setText(state)
            if state == "not configured":  # selected but not configured
                self.labelsPins[index].setStyleSheet('color: red')
            else:
                self.labelsPins[index].setStyleSheet('color: green')


    def browse(self):
        self.path = QtGui.QFileDialog.getExistingDirectory(self, "Select Folder", "")#return the path of the selected folder
        self.Output_Folder_Path_LineEdit.setText(self.path)

    def SaveCurrentPinsConfigToDict(self):
        if self.Input_button.isChecked():
            if self.Pull_Up_button.isChecked():
                state = "Input PullUp"
            elif self.Pull_Imp_button.isChecked():
                state = "Input PullImp"
        elif self.Output_button.isChecked():
            if self.High_button.isChecked():
                state = "Output High"
            elif self.Low_button.isChecked():
                state = "Output Low"
        else:
            state = "not configured"

        for index in range(31):
            if self.checkboxesPins[index].isChecked():
                if state =="not configured": # selected but not configured
                    self.pins_dict[str(index)] = state
                else :
                    self.pins_dict[str(index)]=state
                self.checkboxesPins[index].setChecked(False)
        self.apply_pinsLabels()


    def NewPinsConfiguration(self):
        self.pins_dict = self.pins_dict_init
        for i in self.checkboxesPins :
            i.setChecked(False)
        self.apply_pinsLabels()

    def LoadPinsConfigurationFromFile(self):
        filepath = QtGui.QFileDialog.getOpenFileName(self, 'Single File', "", '*.txt')
        self.pins_dict = eval(open(filepath, 'r').read())
        if not self.pins_dict:
            print ("File is Empty")
        else:
            self.apply_pinsLabels()
                    

    def SavePinsConfigurationToFile(self):
        filepath = QtGui.QFileDialog.getSaveFileName(self, 'Save Point', "", '*.txt')
        file = open(filepath ,'w')
        file.write(str(self.pins_dict))
        file.close()

    def GenerateFun(self):
        outputFolder = self.Output_Folder_Path_LineEdit.text()
        DIO_Config_File = outputFolder+'DIO_Config_File.h'
        MFIC_File = outputFolder+'MFIC.h'
        DIO_File_handler = open("DIO_Config_File",'w')
        MFIC_File_handler = open("MFIC.h",'w')   
      
        pin_mode=""
        index=0

        for pin in self.pins_dict:
            pin_mode=pin[1]
            DIO_File_handler.write(r'#define DIO_u8_'+pin+'PIN0_Mode      '+pin_mode)
            MFIC_File_handler.write(r'#define   '+pin+index)
            index+=1
      
        DIO_File_handler.close()
        MFIC_File_handler.close()
    def resource_path(self, relative_path):#used in .exe extraction
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


        #

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('mohsen.jpg'))
    main = Main()
    main.show()
    sys.exit(app.exec_())


##what is still needed to do
"""
complete SavePinsConfiguration , GenerateFun Functions so that when you check number of pins in checkbox 
you go in loop to save these pins  configuration in a dictionary or any tuples or lists 
so that when we press  a final save button it iterate over this dictionary to save files in self.path 
///and when press on save current button labels which is next to checkboxes should update status 
"""
