from PyQt5.QtCore import QEvent, pyqtSignal
from PyQt5.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QPushButton,
    QStyle,
    QVBoxLayout,
    QWidget,
)


class Sidebar(QWidget):
    """Slim sidebar: mặc định thu gọn, hover để mở rộng."""

    menu_clicked = pyqtSignal(str)
    toggled = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.is_collapsed = True
        self.setObjectName("SidebarPanel")

        self._init_ui()
        self._apply_collapsed_state()

    def _init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(8)

        top_row = QHBoxLayout()
        self.btn_toggle = QPushButton("=")
        self.btn_toggle.setObjectName("GhostButton")
        self.btn_toggle.clicked.connect(self.toggle_sidebar)
        top_row.addWidget(self.btn_toggle)
        top_row.addStretch()
        root.addLayout(top_row)

        self.group = QButtonGroup(self)
        self.group.setExclusive(True)

        self.btn_dashboard = self._create_nav_button(
            "Dashboard",
            self.style().standardIcon(QStyle.SP_DesktopIcon),
            "dashboard",
        )
        self.btn_camera = self._create_nav_button(
            "Camera",
            self.style().standardIcon(QStyle.SP_ComputerIcon),
            "camera",
        )
        self.btn_employee = self._create_nav_button(
            "Nhan su",
            self.style().standardIcon(QStyle.SP_FileDialogDetailedView),
            "employee",
        )
        self.btn_report = self._create_nav_button(
            "Bao cao",
            self.style().standardIcon(QStyle.SP_FileDialogInfoView),
            "report",
        )

        self.btn_dashboard.setChecked(True)

        root.addWidget(self.btn_dashboard)
        root.addWidget(self.btn_camera)
        root.addWidget(self.btn_employee)
        root.addWidget(self.btn_report)
        root.addStretch()

    def _create_nav_button(self, text, icon, key: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setIcon(icon)
        btn.setCheckable(True)
        btn.setObjectName("NavButton")
        btn.setProperty("navText", text)
        btn.clicked.connect(lambda: self.menu_clicked.emit(key))
        self.group.addButton(btn)
        return btn

    def toggle_sidebar(self):
        self.is_collapsed = not self.is_collapsed
        self._apply_collapsed_state()

    def enterEvent(self, event):
        super().enterEvent(event)
        if self.is_collapsed:
            self.is_collapsed = False
            self._apply_collapsed_state()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        if not self.is_collapsed:
            self.is_collapsed = True
            self._apply_collapsed_state()

    def event(self, e):
        if e.type() == QEvent.ToolTip:
            return True
        return super().event(e)

    def _apply_collapsed_state(self):
        for button in [self.btn_dashboard, self.btn_camera, self.btn_employee, self.btn_report]:
            text = button.property("navText")
            if self.is_collapsed:
                button.setText("")
                button.setToolTip(text)
            else:
                button.setText(text)
                button.setToolTip("")

        self.toggled.emit(self.is_collapsed)
