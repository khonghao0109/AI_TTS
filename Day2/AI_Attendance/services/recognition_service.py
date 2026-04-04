from core.face_recognizer import FaceRecognizer


class RecognitionService:
    def __init__(self):
        self.recognizer = FaceRecognizer()

    def recognize(self, face_img):
        return self.recognizer.predict(face_img)
