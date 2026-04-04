from core.face_recognizer import FaceRecognizer


class TrainingService:
    def __init__(self):
        self.recognizer = FaceRecognizer()

    def train(self) -> bool:
        return self.recognizer.train()
