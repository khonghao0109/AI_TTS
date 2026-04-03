import cv2
import json

MODEL_PATH = "data/models/face_model.xml"
LABEL_PATH = "data/models/labels.json"

CONFIDENCE_THRESHOLD = 80  # càng thấp càng chính xác


class RecognitionService:
    def __init__(self):
        self.model = cv2.face.LBPHFaceRecognizer_create()
        self.model.read(MODEL_PATH)

        with open(LABEL_PATH, "r") as f:
            self.label_map = json.load(f)

    def recognize(self, face_img):
        face_img = cv2.resize(face_img, (200, 200))

        label, confidence = self.model.predict(face_img)

        if confidence > CONFIDENCE_THRESHOLD:
            return "Unknown", confidence

        user_id = self.label_map.get(str(label), "Unknown")

        return user_id, confidence