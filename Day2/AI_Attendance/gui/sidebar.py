# gui/sidebar.py
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal

class Sidebar(QWidget):
    menu_clicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        btn_dashboard = QPushButton("Dashboard")
        btn_camera = QPushButton("Camera")
        btn_employee = QPushButton("Nhân sự")

        layout.addWidget(btn_dashboard)
        layout.addWidget(btn_camera)
        layout.addWidget(btn_employee)
        layout.addStretch()

        self.setLayout(layout)

        btn_dashboard.clicked.connect(lambda: self.menu_clicked.emit("dashboard"))
        btn_camera.clicked.connect(lambda: self.menu_clicked.emit("camera"))
        btn_employee.clicked.connect(lambda: self.menu_clicked.emit("employee"))