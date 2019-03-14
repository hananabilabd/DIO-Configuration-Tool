from PyQt4.uic import loadUiType
from PyQt4 import  QtGui ,uic,QtCore
from PyQt4.QtGui import *

#from PySide import  QtGui ,uic,QtCore
#from PySide.QtGui import *

#from PySide import QtCore, QtGui
import sys, os

pins_dict={
    
            "Pin_0":["Output","High"],     
            "Pin_1":["Output","High"],
            "Pin_2":["Output","High"],
            "Pin_3":["Output","High"],
            "Pin_4":["Output","High"],
            "Pin_5":["Output","High"],
            "Pin_6":["Output","High"],
            "Pin_7":["Output","High"],

            "Pin_8":["Output","High"],
            "Pin_9":["Output","High"],
            "Pin_10":["Output","High"],
            "Pin_11":["Output","High"],
            "Pin_12":["Output","High"],
            "Pin_13":["Output","High"],
            "Pin_14":["Output","High"],
            "Pin_15":["Output","High"],

            "Pin_16":["Output","High"],
            "Pin_17":["Output","High"],
            "Pin_18":["Output","High"],
            "Pin_19":["Output","High"],
            "Pin_20":["Output","High"],
            "Pin_21":["Output","High"],
            "Pin_22":["Output","High"],
            "Pin_23":["Output","High"],

            "Pin_24":["Output","High"],
            "Pin_25":["Output","High"],
            "Pin_26":["Output","High"],
            "Pin_27":["Output","High"],
            "Pin_28":["Output","High"],
            "Pin_29":["Output","High"],
            "Pin_30":["Output","High"],
            "Pin_31":["Output","High"]
        };

class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__()
        uic.loadUi(self.resource_path('DIO_config_Tool.ui'), self)
        pixmap = QPixmap("sobhy.jpg")
        self.label_image.setPixmap(pixmap)
        self.label_image.setScaledContents(True)
        self.pushButton_SaveCurrent.clicked.connect(self.SavePinsConfiguration)
        self.pushButton_Browse.clicked.connect(self.browse)
        self.pushButton_FinalSave.setStyleSheet("background-color: green")  ## This is to change Button Color
        self.checkboxesPins=[
            self.checkBox,self.checkBox_2,self.checkBox_3,self.checkBox_4,self.checkBox_5,self.checkBox_6,self.checkBox_7 ,self.checkBox_8,\
            self.checkBox_9,self.checkBox_10,self.checkBox_11,self.checkBox_12,self.checkBox_13,self.checkBox_14,self.checkBox_15,self.checkBox_16, \
            self.checkBox_17, self.checkBox_18, self.checkBox_19,self.checkBox_20, self.checkBox_21,self.checkBox_22,self.checkBox_23,self.checkBox_24,\
            self.checkBox_25, self.checkBox_26,self.checkBox_27, self.checkBox_28,self.checkBox_29,self.checkBox_30,self.checkBox_31,self.checkBox_32]

    def get_SelectedPins(self):
        selectedPins = [i for i in self.checkboxesPins if i.isChecked()]
        return selectedPins

    def browse(self):
        self.path = QtGui.QFileDialog.getExistingDirectory(self, "Select Folder", "")#return the path of the selected folder
        self.Output_Folder_Path_LineEdit.setText(self.path)

    #def SavePinsConfiguration(self):
    #     self.selectedPins=self.get_SelectedPins()

    def SavePinsConfiguration(self):
        type(self.groupBox_Pins)
        print(self.groupBox_Pins)
        selected_pins_list=[]
        
        if self.pushButton_SaveCurrent.isChecked():
        #self.checkbox_1.isClicked()
            for checkbox in self.groupBox_Pins:
                if checkbox.isChecked():
                    selected_pins_list.append(checkbox.text())

                    
            for pin in selected_pins_list:
                if pin in pins_dict: #not sure if right syntax
                    if self.Input_button.isChecked():
                        pins_dict[pin][0]="Input"
                        if self.Pull_Up_button.isChecked():
                            pins_dict[pin][1]="Pull Up"
                        elif self.Pull_Imp_button.isChecked():
                            pins_dict[pin][1]="Pull Down"    


                    elif self.Output_button.isChecked():
                        pins_dict[pin][0]="Output"
                        if self.High_button.isChecked():
                            pins_dict[pin][1]="High"
                        elif self.Low_button.isChecked():
                            pins_dict[pin][1]="Low"  

    def GenerateFun(self):
        outputFolder = self.Output_Folder_Path_LineEdit.text()
        DIO_Config_File = outputFolder+'DIO_Config_File.h'
        MFIC_File = outputFolder+'MFIC.h'
        DIO_File_handler = open("DIO_Config_File",'w')
        MFIC_File_handler = open("MFIC.h",'w')   
      
        pin_mode=""
        index=0

        for pin in pins_dict:
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
