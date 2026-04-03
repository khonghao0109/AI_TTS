import cv2
import os
import numpy as np
from config import MODELS_DIR, DATASET_DIR
from core.utils import create_dir

class FaceRecognizer:
    def __init__(self):
        create_dir(MODELS_DIR)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create(radius=2, neighbors=8, grid_x=8, grid_y=8)
        self.model_path = os.path.join(MODELS_DIR, "face_model.yml")
        self.label_to_user = {}
        self.is_trained = False
        self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            self.recognizer.read(self.model_path)
            self.is_trained = True
            print("✅ Đã load model face recognition từ lần train trước")

    def train(self) -> bool:
        print("🔄 Đang train model...")
        faces, labels = [], []
        self.label_to_user = {}
        label_id = 0

        for user_folder in os.listdir(DATASET_DIR):
            user_path = os.path.join(DATASET_DIR, user_folder)
            if os.path.isdir(user_path):
                self.label_to_user[label_id] = user_folder
                for img_name in os.listdir(user_path):
                    if img_name.endswith(".jpg"):
                        img = cv2.imread(os.path.join(user_path, img_name), cv2.IMREAD_GRAYSCALE)
                        if img is not None:
                            faces.append(img)
                            labels.append(label_id)
                label_id += 1

        if len(faces) < 10:
            print("❌ Cần ít nhất 10 ảnh để train!")
            return False

        self.recognizer.train(faces, np.array(labels))
        self.recognizer.save(self.model_path)
        self.is_trained = True
        print(f"✅ Train thành công {len(faces)} ảnh!")
        return True

    def predict(self, face_crop):
        if not self.is_trained or face_crop is None or face_crop.size == 0:
            return "Unknown", 999

        try:
            gray = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)                    # Tăng độ tương phản
            gray = cv2.resize(gray, (100, 100))

            label, confidence = self.recognizer.predict(gray)
            if label in self.label_to_user and confidence < 90:   # Ngưỡng cao hơn
                return self.label_to_user[label], confidence
            return "Unknown", confidence
        except:
            return "Unknown", 999