import os
import cv2
import json
import numpy as np
from config import DATASET_DIR

MODEL_PATH = "data/models/face_model.xml"
LABEL_PATH = "data/models/labels.json"


class TrainingService:
    def train(self):
        faces = []
        labels = []

        label_map = {}
        current_label = 0

        for user_id in os.listdir(DATASET_DIR):
            user_path = os.path.join(DATASET_DIR, user_id)

            if not os.path.isdir(user_path):
                continue

            label_map[current_label] = user_id

            for file in os.listdir(user_path):
                img_path = os.path.join(user_path, file)

                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    continue

                img = cv2.resize(img, (200, 200))

                faces.append(img)
                labels.append(current_label)

            current_label += 1

        print(f"📊 Total images: {len(faces)}")

        if not faces:
            raise Exception("No dataset found!")

        model = cv2.face.LBPHFaceRecognizer_create()
        model.train(faces, np.array(labels))

        os.makedirs("data/models", exist_ok=True)
        model.save(MODEL_PATH)

        with open(LABEL_PATH, "w") as f:
            json.dump(label_map, f, indent=4)

        return True