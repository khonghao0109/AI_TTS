import os
import tempfile
import threading
import time

import cv2
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage

from config import DATA_DIR
from core.camera import Camera
from core.face_detector import FaceDetector
from core.face_recognizer import FaceRecognizer
from services.dataset_service import DatasetService


class CameraWorker(QObject):
    """Worker chay trong thread rieng de camera khong block UI."""

    frame_ready = pyqtSignal(QImage)
    recognized = pyqtSignal(str)
    log_event = pyqtSignal(str)
    status_changed = pyqtSignal(str)
    collect_finished = pyqtSignal(int)
    training_finished = pyqtSignal(bool)
    error_raised = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.running = False
        self.collecting = False
        self.current_user_id = ""
        self.video_writer = None
        self.video_path = ""
        self.last_recognized_at: dict[str, float] = {}

        self.camera = None
        self.detector = None
        self.recognizer = None
        self.dataset_service = None

        self._is_shutting_down = False
        self._cmd_lock = threading.Lock()
        self._pending_collect_user: str | None = None
        self._pending_stop_collect = False
        self._pending_train = False

    def _safe_emit(self, signal_name: str, *args):
        """Emit signal an toan de tranh crash khi QObject da bi giai phong."""
        if self._is_shutting_down:
            return
        try:
            signal = getattr(self, signal_name)
            signal.emit(*args)
        except RuntimeError:
            self._is_shutting_down = True
            self.running = False

    @pyqtSlot()
    def start(self):
        """Khoi chay vong lap camera trong worker thread."""
        try:
            self.camera = Camera()
            self.detector = FaceDetector()
            self.recognizer = FaceRecognizer()
            self.dataset_service = DatasetService()
        except Exception as exc:
            self._safe_emit("error_raised", str(exc))
            return

        self.running = True
        self._safe_emit("status_changed", "Camera started")

        while self.running:
            self._process_pending_commands()

            frame = self.camera.get_frame()
            if frame is None:
                QThread.msleep(30)
                continue

            display = frame.copy()

            if self.collecting and self.video_writer is not None:
                self.video_writer.write(frame)

            faces = self.detector.detect(display)
            if len(faces) > 0:
                x, y, w, h = faces[0]
                cv2.rectangle(display, (x, y), (x + w, y + h), (52, 152, 219), 2)

                face_crop = display[y : y + h, x : x + w]
                user_id, conf = self.recognizer.predict(face_crop)

                if user_id != "Unknown":
                    text = f"{user_id} ({conf:.0f})"
                    cv2.putText(
                        display,
                        text,
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.65,
                        (46, 204, 113),
                        2,
                    )

                    now = time.time()
                    if user_id not in self.last_recognized_at or now - self.last_recognized_at[user_id] > 2:
                        self.last_recognized_at[user_id] = now
                        self._safe_emit("recognized", user_id)
                        self._safe_emit("log_event", f"{user_id} - recognized")
                else:
                    cv2.putText(
                        display,
                        "Unknown",
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.65,
                        (231, 76, 60),
                        2,
                    )

            rgb = cv2.cvtColor(display, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            image = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888).copy()
            self._safe_emit("frame_ready", image)

            QThread.msleep(30)

        self._release_resources()

    def _start_collect(self, user_id: str):
        if not user_id:
            self._safe_emit("error_raised", "Nhap user ID")
            return

        if self.collecting:
            return

        self.current_user_id = user_id
        self.collecting = True
        os.makedirs(DATA_DIR, exist_ok=True)

        fd, path = tempfile.mkstemp(prefix="capture_", suffix=".avi", dir=DATA_DIR)
        os.close(fd)
        self.video_path = path

        self.video_writer = cv2.VideoWriter(
            self.video_path,
            cv2.VideoWriter_fourcc(*"XVID"),
            30.0,
            (640, 480),
        )
        self._safe_emit("status_changed", "Dang ghi video...")

    def _stop_collect(self):
        if not self.collecting:
            return

        self.collecting = False

        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None

        count = 0
        try:
            if self.video_path and os.path.exists(self.video_path):
                count = self.dataset_service.save_faces_from_video(self.video_path, self.current_user_id)
        except Exception as exc:
            self._safe_emit("error_raised", str(exc))
        finally:
            if self.video_path and os.path.exists(self.video_path):
                os.remove(self.video_path)
            self.video_path = ""

        self._safe_emit("status_changed", "Hoan tat")
        self._safe_emit("collect_finished", count)

    def _train_model(self):
        ok = False
        try:
            ok = self.recognizer.train()
        except Exception as exc:
            self._safe_emit("error_raised", str(exc))
        self._safe_emit("training_finished", ok)

    def enqueue_start_collect(self, user_id: str):
        with self._cmd_lock:
            self._pending_collect_user = user_id

    def enqueue_stop_collect(self):
        with self._cmd_lock:
            self._pending_stop_collect = True

    def enqueue_train(self):
        with self._cmd_lock:
            self._pending_train = True

    def _process_pending_commands(self):
        collect_user = None
        stop_collect = False
        train_model = False

        with self._cmd_lock:
            if self._pending_collect_user is not None:
                collect_user = self._pending_collect_user
                self._pending_collect_user = None
            if self._pending_stop_collect:
                stop_collect = True
                self._pending_stop_collect = False
            if self._pending_train:
                train_model = True
                self._pending_train = False

        if collect_user is not None:
            self._start_collect(collect_user)
        if stop_collect:
            self._stop_collect()
        if train_model:
            self._train_model()

    @pyqtSlot()
    def stop(self):
        self.running = False
        self.collecting = False
        self._is_shutting_down = True

    def _release_resources(self):
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None

        if self.camera is not None:
            self.camera.release()
            self.camera = None


class CameraController(QObject):
    """Controller quan ly vong doi worker/thread cho CameraView."""

    frame_ready = pyqtSignal(QImage)
    recognized = pyqtSignal(str)
    log_event = pyqtSignal(str)
    status_changed = pyqtSignal(str)
    collect_finished = pyqtSignal(int)
    training_finished = pyqtSignal(bool)
    error_raised = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.thread = QThread()
        self.worker = CameraWorker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.start)

        self.worker.frame_ready.connect(self.frame_ready)
        self.worker.recognized.connect(self.recognized)
        self.worker.log_event.connect(self.log_event)
        self.worker.status_changed.connect(self.status_changed)
        self.worker.collect_finished.connect(self.collect_finished)
        self.worker.training_finished.connect(self.training_finished)
        self.worker.error_raised.connect(self.error_raised)

    def start(self):
        if not self.thread.isRunning():
            self.thread.start()

    def request_collect(self, user_id: str):
        self.worker.enqueue_start_collect(user_id)

    def request_stop_collect(self):
        self.worker.enqueue_stop_collect()

    def request_train(self):
        self.worker.enqueue_train()

    def stop(self):
        if self.thread.isRunning():
            self.worker.stop()
            self.thread.quit()
            self.thread.wait(3000)
