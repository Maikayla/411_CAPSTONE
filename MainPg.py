from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QStackedWidget,QTextBrowser,QMenu,QMenuBar,QAction,QStatusBar,QToolBar,QPushButton,QRadioButton,QLabel
from PyQt5 import uic
import sys

class MindPrint_UI(QMainWindow):
    def __init__(self):
        super(MindPrint_UI, self).__init__()

        #Load the UI file
        uic.loadUi("MainPage.ui", self)

        #Define Widgets
        self.Pages = self.findChild(QStackedWidget, "Pages")
        self.Home_page = self.findChild(QWidget, "Home_page")
        self.homepg_title = self.findChild(QTextBrowser, "homepg_title")
        self.Streams_page = self.findChild(QWidget, "Streams_page")
        self.streamspg_title = self.findChild(QTextBrowser, "streamspg_title")
        self.Editing_page = self.findChild(QWidget, "Editing_page")
        self.editpg_title = self.findChild(QTextBrowser, "editpg_title")
        self.Preprocessing_page = self.findChild(QWidget, "Preprocessing_page")
        self.prepropg_title = self.findChild(QTextBrowser, "prepropg_title")
        self.DetectingPatterns_page = self.findChild(QWidget, "DetectingPatterns_page")
        self.detectpattpg_title = self.findChild(QTextBrowser, "detectpattpg_title")
        self.menubar = self.findChild(QMenuBar, "menubar")
        self.menuMenu = self.findChild(QMenu, "menuMenu")
        self.menuStreams = self.findChild(QMenu, "menuStreams")
        self.menuEditing = self.findChild(QMenu, "menuEditing")
        self.menuPreprocessing = self.findChild(QMenu, "menuPreprocessing")
        self.statusbar = self.findChild(QStatusBar, "statusbar")
        self.toolBar = self.findChild(QToolBar, "toolBar")
        self.readStreams_widget = self.findChild(QWidget, "readStreams_widget")

        self.read_pushButton = self.findChild(QPushButton, "read_pushButton")
        #self.radioButton = self.findChild(QRadioButton, "radioButton")
        #self.radioButton_2 = self.findChild(QRadioButton, "radioButton_2")
        #self.radioButton_3 = self.findChild(QRadioButton, "radioButton_3")
        #self.label_2 = self.findChild(QLabel, "label_2")

        #set home page as default
        self.Pages.setCurrentIndex(0)

        #connect "go home" button
        self.actionGoHome.triggered.connect(self.GoHome_clicked)

        #connect "go to streams" button
        self.actionGoToStreams.triggered.connect(self.GoStreams_clicked)

        #connect "go to edit" button
        self.actionGoToEdit_Streams.triggered.connect(self.GoEdit_clicked)

        #connect "go to preprocessing" button
        self.actionGoToPreprocess_pg.triggered.connect(self.GoPreProcess_clicked)

        #connect "go to detecting patterns" button
        self.actionGoToDetect_patterns.triggered.connect(self.GoDetectPatt_clicked)

        #connect "read in streams" button
        self.read_pushButton.clicked.connect(self.select)




        #Show the app
        self.show()

    #functions for clicking toolbar buttons
    def GoHome_clicked(self):
        self.Pages.setCurrentIndex(0)
    def GoStreams_clicked(self):
        self.Pages.setCurrentIndex(1)
    def GoEdit_clicked(self):
        self.Pages.setCurrentIndex(2)
    def GoPreProcess_clicked(self):
        self.Pages.setCurrentIndex(3)
    def GoDetectPatt_clicked(self):
        self.Pages.setCurrentIndex(4)

    #function for radio buttons - reading in streams
    def select(self):
        if self.radioButton.isChecked():
            #read in streams - XDF
            self.label_2.setText("Success for XDF!")

        if self.radioButton_2.isChecked():
            #read in streams - BDF
            self.label_2.setText("Success for BDF!")

        if self.radioButton_3.isChecked():
            #read in streams - CSV
            self.label_2.setText("Success for CSV!")


#Initialize the app
app = QApplication(sys.argv)
UIWindow = MindPrint_UI()
app.exec_()