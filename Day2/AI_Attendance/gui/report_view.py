from datetime import datetime

from PyQt5.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from controllers.report_controller import ReportController


class ReportView(QWidget):
    """Màn hình báo cáo attendance theo tháng/năm cho từng nhân viên."""

    def __init__(self):
        super().__init__()
        self.controller = ReportController()
        self._employee_ids: list[str] = []
        self._init_ui()
        self.reload_filters()

    def _init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        title = QLabel("Bao cao")
        title.setStyleSheet("font-size: 22px; font-weight: 700;")
        root.addWidget(title)

        filter_card = QFrame()
        filter_card.setObjectName("Card")
        filter_layout = QHBoxLayout(filter_card)
        filter_layout.setContentsMargins(12, 10, 12, 10)
        filter_layout.setSpacing(8)

        self.employee_combo = QComboBox()
        self.month_combo = QComboBox()
        self.year_combo = QComboBox()
        self.btn_apply = QPushButton("Xem bao cao")
        self.btn_apply.setObjectName("PrimaryButton")

        for m in range(1, 13):
            self.month_combo.addItem(f"Thang {m}", m)
        current_year = datetime.now().year
        for y in range(current_year - 3, current_year + 2):
            self.year_combo.addItem(str(y), y)
        self.year_combo.setCurrentText(str(current_year))
        self.month_combo.setCurrentIndex(datetime.now().month - 1)

        filter_layout.addWidget(self.employee_combo, 2)
        filter_layout.addWidget(self.month_combo, 1)
        filter_layout.addWidget(self.year_combo, 1)
        filter_layout.addWidget(self.btn_apply)
        root.addWidget(filter_card)

        summary_card = QFrame()
        summary_card.setObjectName("Card")
        summary_layout = QGridLayout(summary_card)
        summary_layout.setContentsMargins(12, 12, 12, 12)
        summary_layout.setHorizontalSpacing(12)
        summary_layout.setVerticalSpacing(10)

        self.label_workdays = QLabel("0")
        self.label_late = QLabel("0")
        self.label_early = QLabel("0")
        self.label_punctual = QLabel("0%")

        self._add_metric(summary_layout, "Tong ngay cong", self.label_workdays, 0, 0)
        self._add_metric(summary_layout, "Tong di muon", self.label_late, 0, 1)
        self._add_metric(summary_layout, "Tong ve som", self.label_early, 1, 0)
        self._add_metric(summary_layout, "Ty le dung gio", self.label_punctual, 1, 1)
        root.addWidget(summary_card)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Ngay", "Gio vao", "Gio ra", "Trang thai", "Ghi chu"])
        self.table.horizontalHeader().setStretchLastSection(True)
        root.addWidget(self.table, stretch=1)

        self.btn_apply.clicked.connect(self.load_report)

    def _add_metric(self, layout: QGridLayout, title: str, value_label: QLabel, row: int, col: int):
        wrapper = QFrame()
        wrapper.setObjectName("Card")
        vbox = QVBoxLayout(wrapper)
        vbox.setContentsMargins(10, 10, 10, 10)

        label_title = QLabel(title)
        label_title.setStyleSheet("color: #94A3B8;")
        value_label.setStyleSheet("font-size: 24px; font-weight: 700; color: #60A5FA;")

        vbox.addWidget(label_title)
        vbox.addWidget(value_label)
        layout.addWidget(wrapper, row, col)

    def reload_filters(self):
        options = self.controller.get_employee_options()
        self._employee_ids = [uid for uid, _ in options]
        self.employee_combo.clear()
        for _, display in options:
            self.employee_combo.addItem(display)
        if options:
            self.load_report()

    def load_report(self):
        if not self._employee_ids:
            return

        idx = self.employee_combo.currentIndex()
        if idx < 0:
            return

        user_id = self._employee_ids[idx]
        month = int(self.month_combo.currentData())
        year = int(self.year_combo.currentData())

        data = self.controller.get_month_report(user_id=user_id, year=year, month=month)
        summary = data["summary"]
        details = data["details"]

        self.label_workdays.setText(str(summary["total_workdays"]))
        self.label_late.setText(str(summary["total_late"]))
        self.label_early.setText(str(summary["total_early"]))
        self.label_punctual.setText(f"{summary['punctuality']}%")

        self.table.setRowCount(0)
        for row_idx, row in enumerate(details):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(row["date"]))
            self.table.setItem(row_idx, 1, QTableWidgetItem(row["check_in_time"]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(row["check_out_time"]))
            self.table.setItem(row_idx, 3, QTableWidgetItem(row["status"]))
            self.table.setItem(row_idx, 4, QTableWidgetItem(row["note"]))
