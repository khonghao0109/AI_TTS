from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from services.employee_service import EmployeeService
import cv2
import time
import os

from core.camera import Camera
from core.face_detector import FaceDetector
from core.face_recognizer import FaceRecognizer
from services.dataset_service import DatasetService
from services.attendance_service import AttendanceService


class CameraView(QWidget):
    def __init__(self):
        super().__init__()

        # ===== SERVICES =====
        self.camera = Camera()
        self.detector = FaceDetector()
        self.recognizer = FaceRecognizer()
        self.dataset_service = DatasetService()
        self.attendance_service = AttendanceService()
        self.employee_service = EmployeeService()

        self.user_id = ""
        self.last_attendance = {}

        # ===== COLLECT =====
        self.collecting = False
        self.video_writer = None
        self.video_path = "temp_video.avi"

        self.build_ui()

        # ===== TIMER =====
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def build_ui(self):
        main_layout = QVBoxLayout(self)

        # ===== TOP =====
        top_layout = QHBoxLayout()

        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("Nhập User ID")

        self.btn_collect = QPushButton("📷 Thu thập 5s")
        self.btn_train = QPushButton("🧠 Train")

        top_layout.addWidget(self.input_id)
        top_layout.addWidget(self.btn_collect)
        top_layout.addWidget(self.btn_train)

        # ===== VIDEO =====
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("background: black;")
        self.video_label.setMinimumHeight(400)

        # ===== INFO =====
        self.status_label = QLabel("Ready")
        self.count_label = QLabel("Số ảnh: 0")
        self.recognized_label = QLabel("Model chưa train")

        # ===== LOG =====
        self.log_list = QListWidget()
        self.log_list.setMaximumHeight(120)

        # ===== ADD =====
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.video_label, stretch=1)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.count_label)
        main_layout.addWidget(self.recognized_label)
        main_layout.addWidget(self.log_list)

        # ===== EVENTS =====
        self.btn_collect.clicked.connect(self.start_collect)
        self.btn_train.clicked.connect(self.train_model)
        self.input_id.textChanged.connect(self.on_user_change)

    def on_user_change(self):
        self.user_id = self.input_id.text().strip()

    # ================= CAMERA =================
    def update_frame(self):
        frame = self.camera.get_frame()
        if frame is None:
            return

        display = frame.copy()

        if self.collecting and self.video_writer:
            self.video_writer.write(frame)

        faces = self.detector.detect(display)

        if len(faces) > 0:
            x, y, w, h = faces[0]
            cv2.rectangle(display, (x, y), (x + w, y + h), (0, 255, 0), 2)

            face_crop = display[y:y + h, x:x + w]
            user_id, conf = self.recognizer.predict(face_crop)

            if user_id != "Unknown":
                text = f"{user_id} ({conf:.0f})"
                cv2.putText(display, text, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                now = time.time()
                if user_id not in self.last_attendance or now - self.last_attendance[user_id] > 10:
                    self.attendance_service.mark_attendance(user_id)
                    self.last_attendance[user_id] = now

                    self.recognized_label.setText(f"✅ {user_id}")
                    self.add_log(user_id)
            else:
                cv2.putText(display, "Unknown", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # ===== SHOW =====
        rgb = cv2.cvtColor(display, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(img)
        self.video_label.setPixmap(
            pixmap.scaled(
                self.video_label.width(),
                self.video_label.height(),
                Qt.KeepAspectRatio
            )
        )

    # ================= LOG =================
    def add_log(self, name):
        self.log_list.insertItem(0, f"{name} - OK")
        if self.log_list.count() > 5:
            self.log_list.takeItem(5)

    # ================= COLLECT =================
    def start_collect(self):
        if not self.user_id:
            QMessageBox.warning(self, "Lỗi", "Nhập user ID")
            return

        self.collecting = True
        self.video_writer = cv2.VideoWriter(
            self.video_path,
            cv2.VideoWriter_fourcc(*'XVID'),
            30.0,
            (640, 480)
        )

        self.status_label.setText("Đang ghi video...")

        QTimer.singleShot(5000, self.stop_collect)

    def stop_collect(self):
        self.collecting = False

        if self.video_writer:
            self.video_writer.release()

        count = self.dataset_service.save_faces_from_video(
            self.video_path, self.user_id
        )

        if os.path.exists(self.video_path):
            os.remove(self.video_path)

        self.count_label.setText(f"Số ảnh: {count}")
        self.status_label.setText("Hoàn tất")

    # ================= TRAIN =================
    def train_model(self):
        ok = self.recognizer.train()
        if ok:
            QMessageBox.information(self, "OK", "Train thành công")
        else:
            QMessageBox.warning(self, "Fail", "Chưa đủ data")