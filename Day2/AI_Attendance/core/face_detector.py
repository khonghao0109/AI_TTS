import cv2
from config import HAARCASCADE_PATH
from core.utils import ensure_haarcascade

class FaceDetector:
    """Face Detection bằng Haar Cascade"""
    def __init__(self):
        ensure_haarcascade(HAARCASCADE_PATH)
        self.face_cascade = cv2.CascadeClassifier(HAARCASCADE_PATH)
        if self.face_cascade.empty():
            raise RuntimeError("❌ Không load được Haar Cascade!")

    def detect(self, frame):
        """Trả về list các khuôn mặt (x, y, w, h)"""
        if frame is None:
            return []
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )
        return faces