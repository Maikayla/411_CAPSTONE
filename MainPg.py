from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QStackedWidget,QTextBrowser,QMenu,QMenuBar,QAction,QStatusBar,QToolBar
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

#Initialize the app
app = QApplication(sys.argv)
UIWindow = MindPrint_UI()
app.exec_()