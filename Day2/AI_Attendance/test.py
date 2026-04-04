import cv2
from config import FACE_MODEL_PATH

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(FACE_MODEL_PATH)

print("Load model OK")
