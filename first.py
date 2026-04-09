from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from camera import Ui_SecondMainWindow


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1250, 700)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(350, 100, 700, 400))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.widget.setFont(font)
        self.widget.setStyleSheet("#widget {\n"
                                  "    background-color: rgb(255, 255, 255);\n"
                                  "}\n"
                                  "\n"
                                  "#pushButtonStart {\n"
                                  "    border: 2px solid rgb(45, 134, 134); /* Border color */\n"
                                  "    background-color: rgb(85, 255, 255); /* Button background color */\n"
                                  "    border-radius: 10px; /* Round the corners */\n"
                                  "    padding: 10px; /* Adjust padding for better look */\n"
                                  "    outline: none;\n"
                                  "}\n"
                                  "\n"
                                  "#pushButtonStart:hover {\n"
                                  "    background-color: rgb(65, 235, 235); /* Slightly darker on hover */\n"
                                  "}\n"
                                  "\n"
                                  "#pushButtonStart:pressed {\n"
                                  "    background-color: rgb(45, 205, 205); /* Even darker when pressed */\n"
                                  "}\n"
                                  "")
        self.widget.setObjectName("widget")

        # QLabel to display images
        self.image_label = QtWidgets.QLabel(self.widget)
        self.image_label.setGeometry(QtCore.QRect(70, 100, 400, 200))  # Adjust size and position
        self.image_label.setStyleSheet("background-color: transparent;")  # Transparent background for label
        self.image_label.setScaledContents(True)  # Ensures image scales to QLabel size
        self.image_label.setObjectName("image_label")

        # Push Button
        self.pushButtonStart = QtWidgets.QPushButton(self.widget)
        self.pushButtonStart.setGeometry(QtCore.QRect(178, 350, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.pushButtonStart.setFont(font)
        self.pushButtonStart.setStyleSheet("")
        self.pushButtonStart.setObjectName("pushButtonStart")

        # Label for Welcome Message
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(100, 30, 291, 22))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 794, 28))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Image switching setup
        self.image_paths = ["animaImages/image1.png", "animaImages/image2.png", "animaImages/image3.png", "animaImages/image4.png", "animaImages/image5.png"]  # Replace with your image paths
        self.current_image_index = 0
        self.image_label.setPixmap(QtGui.QPixmap(self.image_paths[self.current_image_index]))

        # Timer to switch images
        self.timer = QTimer(self.centralwidget)
        self.timer.timeout.connect(self.switch_image)
        self.timer.start(2000)  # Switch every 2 seconds

        # Connect the button to the open_second_window method
        self.pushButtonStart.clicked.connect(self.open_second_window)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonStart.setText(_translate("MainWindow", "Get Start"))
        self.label.setText(_translate("MainWindow", "WELCOME TO CHECKOUTAI"))

    def switch_image(self):
        # Update the image index
        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)

        # Set new image without animation
        self.image_label.setPixmap(QtGui.QPixmap(self.image_paths[self.current_image_index]))

    def open_second_window(self):
        self.second_window = QtWidgets.QMainWindow()
        self.ui_second = Ui_SecondMainWindow()  # Create an instance of the second window UI
        self.ui_second.setupUi(self.second_window)  # Set up the second window
        self.second_window.show()  # Show the second window
        #MainWindow.hide()  # Optionally hide the main window
        QtWidgets.qApp.activeWindow().close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())