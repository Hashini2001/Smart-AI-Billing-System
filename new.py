import sys
import cv2
import numpy as np
import tensorflow as tf
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from datetime import datetime

# Load the trained model
model = tf.keras.models.load_model('item_classifier.h5')

# Load class indices from JSON file
with open('class_indices.json', 'r') as json_file:
    class_indices = json.load(json_file)
    class_names = list(class_indices.keys())

# Function to preprocess the image for the model
def preprocess_image(img):
    img = cv2.resize(img, (128, 128))  # Resize image to match model's input shape
    img = img / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(25, 0, 950, 550))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.widget.setFont(font)
        self.widget.setObjectName("widget")

        # Label for displaying the prediction message
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(350, 40, 291, 22))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # Label for showing the camera feed
        self.camera_feed_label = QtWidgets.QLabel(self.widget)
        self.camera_feed_label.setGeometry(QtCore.QRect(220, 70, 450, 500))
        self.camera_feed_label.setObjectName("camera_feed_label")
        self.camera_feed_label.setStyleSheet("background-color: black;")

        # Push button to scan item
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(425, 480, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet(
            "border: 2px solid rgb(45, 134, 134); "
            "background-color: rgb(85, 255, 255); "
            "border-radius: 10px; padding: 10px;"
            "outline: none;"
        )
        
        # Styling for the button hover and press actions
        self.widget.setStyleSheet(
            "#pushButton:hover { background-color: rgb(65, 235, 235); }"
            "#pushButton:pressed { background-color: rgb(45, 205, 205); }"
        )

        # Billing Table
        self.tableWidget = QtWidgets.QTableWidget(self.widget)
        self.tableWidget.setGeometry(QtCore.QRect(45, 161, 501, 221))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(["No", "Item", "Qty", "Price", "Amount"])

        # Date and Time Labels
        self.label_date = QtWidgets.QLabel(self.widget)
        self.label_date.setGeometry(QtCore.QRect(50, 40, 150, 22))
        self.label_time = QtWidgets.QLabel(self.widget)
        self.label_time.setGeometry(QtCore.QRect(50, 70, 150, 22))

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 28))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Setup timer for updating the camera feed and date/time
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        
        # Open the camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.label.setText("Error: Could not open camera.")
            return
        
        # Start the timer (30 ms interval)
        self.timer.start(30)

        # Connect the push button to capture and predict
        self.pushButton.clicked.connect(self.capture_and_predict)

        # Update date and time every second
        self.update_time()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Billing System"))
        self.pushButton.setText(_translate("MainWindow", "Scan Item"))
        self.label.setText(_translate("MainWindow", "Identifying Item. Please Wait..."))

    def update_frame(self):
        """Updates the camera feed displayed in camera_feed_label."""
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(convert_to_Qt_format)
            self.camera_feed_label.setPixmap(pixmap)

    def capture_and_predict(self):
        """Captures the current frame and processes it for prediction."""
        ret, frame = self.cap.read()
        if ret:
            img = preprocess_image(frame)
            predictions = model.predict(img)
            predicted_class_index = np.argmax(predictions, axis=1)[0]
            predicted_class_name = class_names[predicted_class_index]
            predicted_probability = predictions[0][predicted_class_index]

            self.label.setText(f"Predicted Class: {predicted_class_name}, Probability: {predicted_probability:.4f}")

            # Add item to billing table
            self.add_item_to_billing(predicted_class_name, 1, 10.0)  # Example price, replace with actual price logic
        else:
            self.label.setText("Error: Could not capture frame.")

    def add_item_to_billing(self, item_name, qty, price):
        """Adds the scanned item to the billing table."""
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        self.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(row_position + 1)))
        self.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(item_name))
        self.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(qty)))
        self.tableWidget.setItem(row_position, 3, QtWidgets.QTableWidgetItem(f"{price:.2f}"))
        self.tableWidget.setItem(row_position, 4, QtWidgets.QTableWidgetItem(f"{qty * price:.2f}"))

    def update_time(self):
        """Updates the current date and time on the interface."""
        now = datetime.now()
        self.label_date.setText(now.strftime("Date: %Y-%m-%d"))
        self.label_time.setText(now.strftime("Time: %H:%M:%S"))
        QtCore.QTimer.singleShot(1000, self.update_time)  # Call this method every second

    def closeEvent(self, event):
        """Releases the camera when the window is closed."""
        self.timer.stop()
        self.cap.release()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())