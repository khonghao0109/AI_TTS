from PyQt5.QtWidgets import *

from gui.sidebar import Sidebar
from gui.camera_view import CameraView
from gui.employee_view import EmployeeView
from gui.dashboard_view import DashboardView
from gui.report_view import ReportView
from gui.theme import APP_STYLESHEET


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Attendance System")
        self.resize(1200, 800)
        self.setStyleSheet(APP_STYLESHEET)

        self._init_ui()

    def _init_ui(self):
        main = QWidget()
        self.setCentralWidget(main)

        layout = QHBoxLayout(main)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.setMinimumWidth(72)
        self.sidebar.setMaximumWidth(72)
        layout.addWidget(self.sidebar, 1)

        # Stack
        self.stack = QStackedWidget()
        layout.addWidget(self.stack, 5)

        # Pages
        self.dashboard = DashboardView()
        self.camera = CameraView()
        self.employee = EmployeeView()
        self.report = ReportView()

        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.camera)
        self.stack.addWidget(self.employee)
        self.stack.addWidget(self.report)

        # Event
        self.sidebar.menu_clicked.connect(self.switch_page)
        self.sidebar.toggled.connect(self.on_sidebar_toggled)
        self.dashboard.check_in_requested.connect(self.start_check_in_flow)
        self.dashboard.check_out_requested.connect(self.start_check_out_flow)
        self.camera.attendance_updated.connect(self.dashboard.refresh)
        self.camera.attendance_updated.connect(self.report.reload_filters)
        self.camera.dataset_updated.connect(self.employee.refresh_department_filter)
        self.camera.dataset_updated.connect(self.employee.reload_data)
        self.camera.dataset_updated.connect(self.dashboard.refresh)
        self.on_sidebar_toggled(self.sidebar.is_collapsed)

    def switch_page(self, name):
        mapping = {
            "dashboard": self.dashboard,
            "camera": self.camera,
            "employee": self.employee,
            "report": self.report,
        }

        if name in mapping:
            self.stack.setCurrentWidget(mapping[name])
            if name == "dashboard":
                self.dashboard.refresh()
            if name == "report":
                self.report.reload_filters()

    def on_sidebar_toggled(self, collapsed: bool):
        width = 72 if collapsed else 220
        self.sidebar.setMinimumWidth(width)
        self.sidebar.setMaximumWidth(width)

    def start_check_in_flow(self):
        self.switch_page("camera")
        self.camera.start_attendance_action("check_in")

    def start_check_out_flow(self):
        self.switch_page("camera")
        self.camera.start_attendance_action("check_out")
