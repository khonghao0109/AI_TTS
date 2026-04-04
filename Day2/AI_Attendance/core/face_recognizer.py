import json
import os

import cv2
import numpy as np

from config import DATASET_DIR, FACE_MODEL_PATH, LABELS_PATH
from core.utils import create_dir


class FaceRecognizer:
    def __init__(self):
        create_dir(os.path.dirname(FACE_MODEL_PATH))
        self.recognizer = cv2.face.LBPHFaceRecognizer_create(
            radius=2,
            neighbors=8,
            grid_x=8,
            grid_y=8,
        )
        self.model_path = FACE_MODEL_PATH
        self.labels_path = LABELS_PATH
        self.label_to_user: dict[int, str] = {}
        self.is_trained = False
        self.model_mtime: float | None = None
        self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            try:
                self.recognizer.read(self.model_path)
                labels_ok = self._load_labels()
                self.is_trained = labels_ok
                self.model_mtime = os.path.getmtime(self.model_path)
            except Exception:
                self.label_to_user = {}
                self.is_trained = False
                self.model_mtime = None

    def _load_labels(self):
        if os.path.exists(self.labels_path):
            try:
                with open(self.labels_path, "r", encoding="utf-8") as f:
                    raw = f.read().strip()
                    if not raw:
                        self.label_to_user = {}
                        return False
                    data = json.loads(raw)
                self.label_to_user = {int(k): v for k, v in data.items()}
                return len(self.label_to_user) > 0
            except (json.JSONDecodeError, ValueError, OSError):
                self.label_to_user = {}
                return False
        else:
            self.label_to_user = {}
            return False

    def _save_labels(self):
        with open(self.labels_path, "w", encoding="utf-8") as f:
            json.dump({str(k): v for k, v in self.label_to_user.items()}, f, indent=4)

    def train(self) -> bool:
        faces: list[np.ndarray] = []
        labels: list[int] = []
        self.label_to_user = {}

        if not os.path.exists(DATASET_DIR):
            return False

        label_id = 0
        for user_folder in sorted(os.listdir(DATASET_DIR)):
            user_path = os.path.join(DATASET_DIR, user_folder)
            if not os.path.isdir(user_path):
                continue

            self.label_to_user[label_id] = user_folder

            for img_name in sorted(os.listdir(user_path)):
                if not img_name.lower().endswith(".jpg"):
                    continue

                img_path = os.path.join(user_path, img_name)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    continue

                img = cv2.resize(img, (200, 200))
                faces.append(img)
                labels.append(label_id)

            label_id += 1

        if len(faces) < 10:
            return False

        self._cleanup_old_models()
        self.recognizer.train(faces, np.array(labels))
        self.recognizer.save(self.model_path)
        self._save_labels()
        self.is_trained = True
        self.model_mtime = os.path.getmtime(self.model_path)
        return True

    def _cleanup_old_models(self):
        """
        Xóa các file model cũ trước khi train lại để tránh dùng model stale.
        """
        model_dir = os.path.dirname(self.model_path)
        create_dir(model_dir)
        for name in os.listdir(model_dir):
            lower = name.lower()
            if lower.endswith((".yml", ".yaml", ".xml", ".h5", ".onnx", ".pt", ".pth")):
                try:
                    os.remove(os.path.join(model_dir, name))
                except OSError:
                    pass

    def predict(self, face_crop):
        # Tự động reload model nếu file vừa được train lại ở thread khác.
        if os.path.exists(self.model_path):
            current_mtime = os.path.getmtime(self.model_path)
            if self.model_mtime is None or current_mtime != self.model_mtime:
                self.load_model()

        if not self.is_trained or face_crop is None or face_crop.size == 0:
            return "Unknown", 999

        try:
            if len(face_crop.shape) == 3:
                gray = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
            else:
                gray = face_crop

            gray = cv2.equalizeHist(gray)
            gray = cv2.resize(gray, (200, 200))

            label, confidence = self.recognizer.predict(gray)
            if label in self.label_to_user and confidence < 90:
                return self.label_to_user[label], confidence

            return "Unknown", confidence
        except Exception:
            return "Unknown", 999
