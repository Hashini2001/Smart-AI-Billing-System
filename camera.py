import sys
import cv2
import numpy as np
import tensorflow as tf
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QDateTime


# Load the trained model
model = tf.keras.models.load_model('item_classifier.h5')

item_prices = {
        "kistjam": 290.00,
        "peppermint":40.00,
        "null":0.00
    }


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

class Ui_SecondMainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1250, 700)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        

        # Camera widget setup
        self.camerawidget = QtWidgets.QWidget(self.centralwidget)
        self.camerawidget.setGeometry(QtCore.QRect(525, 10, 700, 600))
        self.camerawidget.setStyleSheet("#camerawidget { background-color: rgb(255, 255, 255); }")
        self.camerawidget.setObjectName("camerawidget")


        # Identity label
        self.IdentityLabel = QtWidgets.QLabel(self.camerawidget)
        self.IdentityLabel.setGeometry(QtCore.QRect(200, 20, 291, 22))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setBold(True)
        font.setWeight(75)
        self.IdentityLabel.setFont(font)
        self.IdentityLabel.setObjectName("IdentityLabel")

        # Camera label
        self.cameraLabel = QtWidgets.QLabel(self.camerawidget)
        self.cameraLabel.setGeometry(QtCore.QRect(80, 50, 500, 475))
        self.cameraLabel.setText("")
        self.cameraLabel.setObjectName("cameraLabel")

        # Scan button setup
        self.scanButton = QtWidgets.QPushButton(self.camerawidget)
        self.scanButton.setGeometry(QtCore.QRect(280, 550, 121, 41))
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setBold(False)
        font.setWeight(50)
        self.scanButton.setFont(font)
        self.scanButton.setObjectName("scanButton")
        self.scanButton.setText("Scan Item")  # Set the button text
        self.scanButton.setStyleSheet(
            "QPushButton {"
            "   border: 2px solid rgb(45, 134, 134);"
            "   background-color: rgb(85, 255, 255);"
            "   border-radius: 10px;"
            "   padding: 10px;"
            "   outline: none;"
            "}"
            "QPushButton:hover {"
            "   background-color: rgb(65, 235, 235);"
            "}"  
            "QPushButton:pressed {"
            "   background-color: rgb(45, 205, 205);"
            "}"  
        )

        # Billing Widget
        self.billingWidget = QtWidgets.QWidget(self.centralwidget)
        self.billingWidget.setGeometry(QtCore.QRect(10, 10, 500, 600))
        self.billingWidget.setObjectName("billingWidget")

        self.label = QtWidgets.QLabel(self.billingWidget)
        self.label.setGeometry(QtCore.QRect(210, 30, 91, 22))
        self.label.setText("Your Bill...")
        # Set font properties
        font = QtGui.QFont()
        font.setBold(True)        
        font.setPointSize(14)     
        self.label.setFont(font) 

        # labels for date and time
        self.dateLabel = QtWidgets.QLabel(self.billingWidget)
        self.dateLabel.setGeometry(QtCore.QRect(50, 90, 200, 22))  # Adjust position and size as needed
        self.dateLabel.setAlignment(QtCore.Qt.AlignCenter)  # Center align the text

        self.timeLabel = QtWidgets.QLabel(self.billingWidget)
        self.timeLabel.setGeometry(QtCore.QRect(200, 90, 200, 22))  # Position below the date label
        self.timeLabel.setAlignment(QtCore.Qt.AlignCenter)  # Center align the text


        self.tableWidget = QtWidgets.QTableWidget(self.billingWidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 150, 441, 251))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)  # Start with 0 rows
        self.tableWidget.setHorizontalHeaderLabels(["Item", "Price", "Qty", "Amount"])

        # Buttons for Quantity and Total Calculation
        self.QtyButton = QtWidgets.QPushButton(self.billingWidget)
        self.QtyButton.setGeometry(QtCore.QRect(20, 450, 111, 40))
        self.QtyButton.setText("Increase Qty")
        self.QtyButton.setStyleSheet(
            "QPushButton {"
            "   border: 2px solid rgb(45, 134, 134);"
            "   background-color: rgb(85, 255, 255);"
            "   border-radius: 10px;"
            "   padding: 10px;"
            "   outline: none;"
            "}"
            "QPushButton:hover {"
            "   background-color: rgb(65, 235, 235);"
            "}"  
            "QPushButton:pressed {"
            "   background-color: rgb(45, 205, 205);"
            "}"  
        )

        self.TotButton = QtWidgets.QPushButton(self.billingWidget)
        self.TotButton.setGeometry(QtCore.QRect(160, 450, 131, 40))
        self.TotButton.setText("Calculate Total")
        self.TotButton.setStyleSheet(
            "QPushButton {"
            "   border: 2px solid rgb(45, 134, 134);"
            "   background-color: rgb(85, 255, 255);"
            "   border-radius: 10px;"
            "   padding: 10px;"
            "   outline: none;"
            "}"
            "QPushButton:hover {"
            "   background-color: rgb(65, 235, 235);"
            "}"  
            "QPushButton:pressed {"
            "   background-color: rgb(45, 205, 205);"
            "}"  
        )

        self.FinishButton = QtWidgets.QPushButton(self.billingWidget)
        self.FinishButton.setGeometry(QtCore.QRect(320, 450, 130, 40))
        self.FinishButton.setText("CheckOut")
        self.FinishButton.setStyleSheet(
            "QPushButton {"
            "   border: 2px solid rgb(45, 134, 134);"
            "   background-color: rgb(85, 255, 255);"
            "   border-radius: 10px;"
            "   padding: 10px;"
            "   outline: none;"
            "}"
            "QPushButton:hover {"
            "   background-color: rgb(65, 235, 235);"
            "}"  
            "QPushButton:pressed {"
            "   background-color: rgb(45, 205, 205);"
            "}"  
        )

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.update_date_time()

        # Timer for date and time
        self.dateTimeTimer = QTimer()
        self.dateTimeTimer.timeout.connect(self.update_date_time)
        self.dateTimeTimer.start(1000)  # Update every second

        # Timer for camera feed
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Open the camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            return

        # Start the timer (30 ms interval)
        self.timer.start(30)

        # Connect buttons
        self.scanButton.clicked.connect(self.capture_and_predict)
        self.QtyButton.clicked.connect(self.increase_qty)
        self.TotButton.clicked.connect(self.calculate_total)

        # Connect the button to the open_second_window method
        self.FinishButton.clicked.connect(self.open_final_window)

        self.current_item = None
        self.current_price = 0.0
        self.current_qty = 1

    def update_date_time(self):
        """Updates the date and time label."""
        current_date_time = QDateTime.currentDateTime()
        # Update the date label
        date_text = current_date_time.toString("yyyy-MM-dd")
        self.dateLabel.setText(date_text)
        
        # Update the time label
        time_text = current_date_time.toString("hh:mm:ss")
        self.timeLabel.setText(time_text)

    def update_frame(self):
        """Updates the camera feed displayed in camera_feed_label."""
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(convert_to_Qt_format)
            self.cameraLabel.setPixmap(pixmap)

    
    def capture_and_predict(self):
        """Captures the current frame and processes it for prediction."""
        ret, frame = self.cap.read()
        if ret:
            img = preprocess_image(frame)
            predictions = model.predict(img)
            predicted_class_index = np.argmax(predictions, axis=1)[0]
            predicted_class_name = class_names[predicted_class_index]
            self.current_item = predicted_class_name
            self.current_price = item_prices.get(predicted_class_name,0.00)
            self.update_bill()

    def update_bill(self):
        """Updates the bill with the current item."""
        # Check if the item is already in the table
        for row in range(self.tableWidget.rowCount()):
            item_name = self.tableWidget.item(row, 0).text()
            if item_name == self.current_item:
                # If item exists, update quantity and amount
                current_qty = int(self.tableWidget.item(row, 2).text())
                new_qty = current_qty + 1
                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(new_qty)))
                amount = new_qty * self.current_price
                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(f"{amount:.2f}"))
                return  # Exit the method after updating

        # If item doesn't exist, add it as a new row
        self.current_qty = 1  # Reset the quantity to 1 for new items
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        self.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(self.current_item))
        self.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(f"{self.current_price:.2f}"))
        self.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(self.current_qty)))
        self.tableWidget.setItem(row_position, 3, QtWidgets.QTableWidgetItem(f"{self.current_price * self.current_qty:.2f}"))

    def increase_qty(self):
        """Increases the quantity of the current item and updates the amount."""
        if self.current_item is not None:
            self.current_qty += 1
            self.update_bill()
        
    def calculate_total(self):
        """Calculates the total of the amount column and displays it."""
        total = 0.0
        for row in range(self.tableWidget.rowCount()):
            amount_item = self.tableWidget.item(row, 3)
            total += float(amount_item.text())
        
        # Check if a total row already exists and remove it
        for row in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(row, 0).text() == "Total":
                self.tableWidget.removeRow(row)
                break  # Exit after removing the total row

        # Add a new row for the total
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        self.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem("Total"))
        self.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(""))  # Price column left blank
        self.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(""))  # Quantity column left blank
        self.tableWidget.setItem(row_position, 3, QtWidgets.QTableWidgetItem(f"{total:.2f}"))  # Total amount

    def finish_transaction(self):
        """Finishes the transaction (placeholder for future functionality)."""
        QtWidgets.QMessageBox.information(None, "Transaction", "Transaction Finished!")

    def closeEvent(self, event):
        """Releases the camera when the window is closed."""
        self.timer.stop()
        self.cap.release()

    def open_final_window(self):
        from final import Ui_FinalMainWindow  # Import here to avoid circular import
        self.final_window = QtWidgets.QMainWindow()
        self.ui_final = Ui_FinalMainWindow()  # Create an instance of the second window UI
        self.ui_final.setupUi(self.final_window)  # Set up the second window
        self.final_window.show()  # Show the second window
        #SecondMainWindow.hide()  # Optionally hide the main window
        QtWidgets.qApp.activeWindow().close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    SecondMainWindow = QtWidgets.QMainWindow()
    ui = Ui_SecondMainWindow()
    ui.setupUi(SecondMainWindow)
    SecondMainWindow.show()
    sys.exit(app.exec_())