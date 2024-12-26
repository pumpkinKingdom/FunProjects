### virtual_closet.py (Main Application - PyQt Frontend)
import sys
import requests
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import cv2
import numpy as np

BACKEND_URL = 'http://127.0.0.1:5000/upload'

class ClosetApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Virtual Closet Organizer')
        self.setGeometry(200, 200, 400, 400)

        self.label = QLabel(self)
        self.label.setText('Upload Closet Photo')
        self.label.setAlignment(Qt.AlignCenter)

        self.upload_button = QPushButton('Upload Closet Photo', self)
        self.upload_button.clicked.connect(self.uploadPhoto)

        self.result_label = QLabel('Recommendations will appear here.', self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def uploadPhoto(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Closet Image", "", "Images (*.png *.xpm *.jpg *.jpeg)", options=options)
        if fileName:
            pixmap = QPixmap(fileName)
            self.label.setPixmap(pixmap.scaled(300, 300))

            # Send to backend
            self.sendToBackend(fileName)

    def sendToBackend(self, fileName):
        with open(fileName, 'rb') as file:
            files = {'file': file}
            response = requests.post(BACKEND_URL, files=files)
            if response.status_code == 200:
                self.result_label.setText(response.json().get('recommendations', 'No recommendations'))
            else:
                self.result_label.setText('Error analyzing photo.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClosetApp()
    window.show()
    sys.exit(app.exec_())

