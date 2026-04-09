from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
#from first import Ui_MainWindow


class Ui_FinalMainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1254, 700)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 1200, 650))
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(500, 100, 341, 51))
        font = QtGui.QFont()
        font.setPointSize(21)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # QLabel to display images
        self.image_label = QtWidgets.QLabel(self.widget)
        self.image_label.setGeometry(QtCore.QRect(450, 200, 400, 200))  # Adjust size and position
        self.image_label.setStyleSheet("background-color: transparent;")  # Transparent background for label
        self.image_label.setScaledContents(True)  # Ensures image scales to QLabel size
        self.image_label.setObjectName("image_label")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1254, 28))
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

        # Timer to switch to the first window after 2 minutes (120000 ms)
        self.switch_timer = QTimer(self.centralwidget)
        self.switch_timer.timeout.connect(self.switch_to_first_window)
        self.switch_timer.setSingleShot(True)  # Only trigger once
        self.switch_timer.start(30000)  # 2 minutes in milliseconds

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Thank You. Come Again..."))

    def switch_image(self):
        # Update the image index
        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)

        # Set new image without animation
        self.image_label.setPixmap(QtGui.QPixmap(self.image_paths[self.current_image_index]))

    def switch_to_first_window(self):
        from first import Ui_MainWindow  # Import here to avoid circular import
        self.first_window = QtWidgets.QMainWindow()  
        self.ui_first = Ui_MainWindow()  
        self.ui_first.setupUi(self.first_window)  
        self.first_window.show()  
        QtWidgets.qApp.activeWindow().close()  


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_FinalMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
