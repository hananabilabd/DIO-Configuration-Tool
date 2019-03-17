#from PyQt4.uic import loadUiType
from PyQt4 import  QtGui ,uic
from PyQt4.QtGui import QMainWindow,QPixmap
#from PySide import  QtGui ,uic,QtCore
#from PySide.QtGui import *
#from PySide import QtCore, QtGui
import sys, os
import resource_rc
class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__()
        uic.loadUi(self.resource_path('DIO_config_Tool.ui'), self)
        # self.setupUi(self)
        # image_rc.qInitResources()
        #pixmap = QPixmap(self.resource_path("sobhy.jpg"))
        #self.label_image.setPixmap(pixmap)
        #self.label_image.setScaledContents(True)
        self.pushButton_SaveCurrent.clicked.connect(self.SaveCurrentPinsConfigToDict)
        self.pushButton_new.clicked.connect(self.NewPinsConfiguration)
        self.pushButton_load.clicked.connect(self.LoadPinsConfigurationFromFile)
        self.pushButton_save.clicked.connect(self.SavePinsConfigurationToFile)
        self.pushButton_BrowseGenerate.clicked.connect(self.browseThenGenerate)
        self.checkboxesPins=self.encodeListNames("self.checkBox_")
        self.labelsPins=self.encodeListNames("self.label_")
        self.pins_dict ={}
        self.init_dict()

    def encodeListNames(self,desiredName):
        #takes arguments like "self.checkBox_" to return list contain from self.checkBox_0 to self.checkBox_31
        l=[desiredName+str(i) for i in range(32)]
        return [eval(i) for i in l ]#evalute objects from string to slef.checkBox_1 for example

    def init_dict(self):
        for i in range (32):
            self.pins_dict[str(i)]="not configured"

    def apply_pinsLabels(self):
        for index in range (31):
            state =self.pins_dict[str(index)]
            self.labelsPins[index].setText(state)
            if state == "not configured":  # selected but not configured
                self.labelsPins[index].setStyleSheet('color: red')
            else:
                self.labelsPins[index].setStyleSheet('color: green')


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
        self.init_dict()
        for i in self.checkboxesPins :
            i.setChecked(False)
        self.apply_pinsLabels()

    def LoadPinsConfigurationFromFile(self):
        filepath = QtGui.QFileDialog.getOpenFileName(self, 'Single File', "", '*.txt')
        if filepath:
            self.pins_dict = eval(open(filepath, 'r').read())
            if not self.pins_dict:
                print ("File is Empty")
            else:
                self.apply_pinsLabels()
                    

    def SavePinsConfigurationToFile(self):
        filepath = QtGui.QFileDialog.getSaveFileName(self, 'Save Point', "", '*.txt')
        if filepath :
            file = open(filepath ,'w')
            file.write(str(self.pins_dict))
            file.close()

    def browseThenGenerate(self):
        self.path = QtGui.QFileDialog.getExistingDirectory(self, "Select Folder","")  # return the path of the selected folder
        if self.path:
            outputFolder = self.path
            self.Output_Folder_Path_LineEdit.setText(self.path+r'\ ')
            DIO_Config_File = outputFolder + r'\DIO_Config_File.h'
            MFIC_File = outputFolder + r'\MFIC.h'
            DIO_File_handler = open(DIO_Config_File, 'w')
            MFIC_File_handler = open(MFIC_File, 'w')
            for index in range(31):
                pin_mode = self.pins_dict[str(index)]
                if pin_mode != "not configured":
                    pin_mode = self.pins_dict[str(index)].replace(' ', '')
                    DIO_File_handler.write(r'#define DIO_u8_PIN' + str(index) + '_Mode      ' + pin_mode + '\n')
                    MFIC_File_handler.write(r'#define DIO_u8_PIN_' + str(index) + '      ' + str(index) + '\n')

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
    main = Main()
    #app.setWindowIcon(QtGui.QIcon(main.resource_path('mohsen.jpg')))
    main.show()
    sys.exit(app.exec_())

