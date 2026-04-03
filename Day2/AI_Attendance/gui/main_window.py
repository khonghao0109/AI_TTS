from PyQt5.QtWidgets import *

from gui.sidebar import Sidebar
from gui.camera_view import CameraView
from gui.employee_view import EmployeeView
from gui.dashboard_view import DashboardView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Attendance System")
        self.resize(1200, 800)

        self._init_ui()

    def _init_ui(self):
        main = QWidget()
        self.setCentralWidget(main)

        layout = QHBoxLayout(main)

        # Sidebar
        self.sidebar = Sidebar()
        layout.addWidget(self.sidebar, 1)

        # Stack
        self.stack = QStackedWidget()
        layout.addWidget(self.stack, 4)

        # Pages
        self.dashboard = DashboardView()
        self.camera = CameraView()
        self.employee = EmployeeView()

        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.camera)
        self.stack.addWidget(self.employee)

        # Event
        self.sidebar.menu_clicked.connect(self.switch_page)

    def switch_page(self, name):
        mapping = {
            "dashboard": self.dashboard,
            "camera": self.camera,
            "employee": self.employee
        }

        if name in mapping:
            self.stack.setCurrentWidget(mapping[name])