from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from controllers.dashboard_controller import DashboardController
from gui.components.attendance_chart import AttendanceChartWidget


class StatCard(QFrame):
    """Card thống kê bo góc, đồng nhất phong cách dashboard."""

    def __init__(self, title: str, color: str):
        super().__init__()
        self.setObjectName("Card")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(6)

        self.label_title = QLabel(title)
        self.label_title.setStyleSheet("font-size: 13px; color: #94A3B8;")

        self.label_value = QLabel("0")
        self.label_value.setStyleSheet(f"font-size: 28px; font-weight: 700; color: {color};")

        layout.addWidget(self.label_title)
        layout.addWidget(self.label_value)


class DashboardView(QWidget):
    """Dashboard có realtime stats + chart tuần + check-in/check-out actions."""

    check_in_requested = pyqtSignal()
    check_out_requested = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.controller = DashboardController()

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(15)

        self.title = QLabel("Dashboard")
        self.title.setStyleSheet("font-size: 22px; font-weight: 700;")
        root.addWidget(self.title)

        action_row = QHBoxLayout()
        self.btn_check_in = QPushButton("Check-in")
        self.btn_check_in.setObjectName("PrimaryButton")

        self.btn_check_out = QPushButton("Check-out")
        self.btn_check_out.setObjectName("DangerButton")

        action_row.addWidget(self.btn_check_in)
        action_row.addWidget(self.btn_check_out)
        action_row.addStretch()
        root.addLayout(action_row)

        self.dashboard_layout = QGridLayout()
        self.dashboard_layout.setContentsMargins(20, 20, 20, 20)
        self.dashboard_layout.setHorizontalSpacing(15)
        self.dashboard_layout.setVerticalSpacing(15)

        self.card_users = StatCard("Total Users", "#60A5FA")
        self.card_images = StatCard("Total Images", "#22D3EE")
        self.card_present = StatCard("Da co mat", "#34D399")
        self.card_late = StatCard("Di muon", "#F59E0B")

        self.chart_card = QFrame()
        self.chart_card.setObjectName("Card")
        chart_layout = QVBoxLayout(self.chart_card)
        chart_layout.setContentsMargins(16, 14, 16, 14)
        chart_layout.setSpacing(8)

        chart_title = QLabel("Attendance This Week")
        chart_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #E2E8F0;")

        self.chart = AttendanceChartWidget()

        chart_layout.addWidget(chart_title)
        chart_layout.addWidget(self.chart)

        self.quick_card = QFrame()
        self.quick_card.setObjectName("Card")
        quick_layout = QVBoxLayout(self.quick_card)
        quick_layout.setContentsMargins(16, 14, 16, 14)
        quick_layout.setSpacing(8)

        quick_title = QLabel("Thong bao nhanh")
        quick_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #E2E8F0;")
        self.quick_info = QLabel()
        self.quick_info.setWordWrap(True)
        self.quick_info.setStyleSheet("color: #94A3B8;")

        quick_layout.addWidget(quick_title)
        quick_layout.addWidget(self.quick_info)
        quick_layout.addStretch()

        # Hàng 1: 4 cards đều nhau trên toàn chiều ngang (12 cột, mỗi card chiếm 3 cột).
        self.dashboard_layout.addWidget(self.card_users, 0, 0, 1, 3)
        self.dashboard_layout.addWidget(self.card_images, 0, 3, 1, 3)
        self.dashboard_layout.addWidget(self.card_present, 0, 6, 1, 3)
        self.dashboard_layout.addWidget(self.card_late, 0, 9, 1, 3)

        # Hàng 2: chart 70% (8/12) + quick widget 30% (4/12).
        self.dashboard_layout.addWidget(self.chart_card, 1, 0, 1, 8)
        self.dashboard_layout.addWidget(self.quick_card, 1, 8, 1, 4)

        for col in range(12):
            self.dashboard_layout.setColumnStretch(col, 1)

        self.dashboard_layout.setRowStretch(0, 1)
        self.dashboard_layout.setRowStretch(1, 2)

        root.addLayout(self.dashboard_layout, 1)

        self.btn_check_in.clicked.connect(self.check_in_requested.emit)
        self.btn_check_out.clicked.connect(self.check_out_requested.emit)

        self.refresh()

    def refresh(self):
        summary = self.controller.get_summary()
        weekly = self.controller.get_weekly_attendance()
        live = self.controller.get_live_stats()

        self.card_users.label_value.setText(str(summary["total_users"]))
        self.card_images.label_value.setText(str(summary["total_images"]))
        self.card_present.label_value.setText(str(live["present"]))
        self.card_late.label_value.setText(str(live["late"]))
        self.quick_info.setText(
            f"- Vang mat hom nay: {live['absent']}\n"
            f"- Tong check-in 7 ngay: {sum(weekly['values'])}\n"
            "- Nhan su moi: Vui long xem tab Nhan su"
        )

        self.chart.set_data(weekly["labels"], weekly["values"])
