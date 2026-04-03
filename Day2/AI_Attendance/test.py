import cv2

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("models/face_model.yml")

print("Load model OK")