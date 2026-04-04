from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QStyle,
    QVBoxLayout,
    QWidget,
)

from controllers.camera_controller import CameraController
from services.attendance_service import AttendanceService


class CameraView(QWidget):
    """Màn hình camera: preview realtime + collect/train + attendance actions."""

    attendance_updated = pyqtSignal()
    dataset_updated = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.controller = CameraController()
        self.attendance_service = AttendanceService()
        self.pending_action: str | None = None
        self.last_action_user = ""

        self._init_ui()
        self._bind_signals()

        self.controller.start()

    def _init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        title = QLabel("Camera")
        title.setStyleSheet("font-size: 22px; font-weight: 700;")
        root.addWidget(title)

        control_card = QFrame()
        control_card.setObjectName("Card")
        control_layout = QHBoxLayout(control_card)
        control_layout.setContentsMargins(12, 10, 12, 10)
        control_layout.setSpacing(8)

        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("Nhap User ID de collect")

        self.btn_collect = QPushButton("Collect 5s")
        self.btn_collect.setObjectName("PrimaryButton")
        self.btn_collect.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))

        self.btn_train = QPushButton("Train Model")
        self.btn_train.setObjectName("GhostButton")
        self.btn_train.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))

        control_layout.addWidget(self.input_id, 2)
        control_layout.addWidget(self.btn_collect)
        control_layout.addWidget(self.btn_train)

        root.addWidget(control_card)

        self.video_frame = QFrame()
        self.video_frame.setObjectName("Card")
        video_layout = QVBoxLayout(self.video_frame)
        video_layout.setContentsMargins(12, 12, 12, 12)

        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setMinimumHeight(420)
        self.video_label.setStyleSheet("background: #020617; border-radius: 12px;")

        video_layout.addWidget(self.video_label)
        root.addWidget(self.video_frame, stretch=1)

        info_row = QHBoxLayout()
        self.status_label = QLabel("Ready")
        self.count_label = QLabel("So anh: 0")
        self.recognized_label = QLabel("Model chua train")

        for label in [self.status_label, self.count_label, self.recognized_label]:
            label.setStyleSheet(
                "background: #111827; border: 1px solid #1F2937; border-radius: 8px; padding: 8px 10px;"
            )
            info_row.addWidget(label)

        root.addLayout(info_row)

        self.log_list = QListWidget()
        self.log_list.setMaximumHeight(140)
        root.addWidget(self.log_list)

    def _bind_signals(self):
        self.btn_collect.clicked.connect(self.start_collect)
        self.btn_train.clicked.connect(self.start_training)

        self.controller.frame_ready.connect(self.on_frame_ready)
        self.controller.recognized.connect(self.on_recognized)
        self.controller.log_event.connect(self.add_log)
        self.controller.status_changed.connect(self.status_label.setText)
        self.controller.collect_finished.connect(self.on_collect_finished)
        self.controller.training_finished.connect(self.on_training_finished)
        self.controller.error_raised.connect(self.on_worker_error)

    def start_attendance_action(self, action: str):
        """
        Kích hoạt chế độ check-in/check-out bằng nhận diện khuôn mặt.
        action: check_in | check_out
        """
        self.pending_action = action
        label = "Check-in" if action == "check_in" else "Check-out"
        self.status_label.setText(f"Attendance mode: {label}. Vui long nhin vao camera")

    def on_frame_ready(self, image):
        pixmap = QPixmap.fromImage(image)
        self.video_label.setPixmap(
            pixmap.scaled(
                self.video_label.width(),
                self.video_label.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )

    def on_recognized(self, user_id: str):
        self.recognized_label.setText(f"Recognized: {user_id}")

        if not self.pending_action:
            return

        if self.last_action_user == user_id:
            return

        self.last_action_user = user_id

        if self.pending_action == "check_in":
            result = self.attendance_service.check_in(user_id)
        else:
            result = self.attendance_service.check_out(user_id)

        self.status_label.setText(result["message"])
        self.add_log(f"{self.pending_action}: {user_id} -> {result['message']}")

        # Mỗi lần nhận diện chỉ xử lý một action, tránh lặp spam theo frame.
        self.pending_action = None
        self.last_action_user = ""

        if result["success"]:
            self.attendance_updated.emit()

    def start_collect(self):
        user_id = self.input_id.text().strip()
        if not user_id:
            QMessageBox.warning(self, "Loi", "Nhap user ID")
            return

        self.btn_collect.setEnabled(False)
        self.controller.request_collect(user_id)
        QTimer.singleShot(5000, self.controller.request_stop_collect)

    def on_collect_finished(self, count: int):
        self.count_label.setText(f"So anh: {count}")
        self.btn_collect.setEnabled(True)
        if count > 0:
            self.dataset_updated.emit()

    def start_training(self):
        self.btn_train.setEnabled(False)
        self.status_label.setText("Dang train...")
        self.controller.request_train()

    def on_training_finished(self, ok: bool):
        self.btn_train.setEnabled(True)
        if ok:
            QMessageBox.information(self, "OK", "Train thanh cong")
            self.recognized_label.setText("Model ready")
            self.dataset_updated.emit()
        else:
            QMessageBox.warning(self, "Fail", "Chua du data de train")

    def on_worker_error(self, message: str):
        QMessageBox.warning(self, "Camera Error", message)
        self.btn_collect.setEnabled(True)
        self.btn_train.setEnabled(True)

    def add_log(self, msg: str):
        self.log_list.insertItem(0, msg)
        if self.log_list.count() > 10:
            self.log_list.takeItem(10)

    def closeEvent(self, event):
        self.controller.stop()
        super().closeEvent(event)
