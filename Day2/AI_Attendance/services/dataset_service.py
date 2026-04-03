import os
import cv2

from config import DATASET_DIR
from core.utils import create_dir
from core.face_detector import FaceDetector
from services.employee_service import EmployeeService


class DatasetService:
    def __init__(self):
        create_dir(DATASET_DIR)
        self.detector = FaceDetector()
        self.employee_service = EmployeeService()

    def save_face(self, frame, face_coords, user_id: str) -> str:
        if frame is None or face_coords is None or len(face_coords) != 4:
            return None

        x, y, w, h = [int(v) for v in face_coords]

        # Crop + resize chuẩn
        face_crop = frame[y:y + h, x:x + w]
        face_crop = cv2.resize(face_crop, (200, 200))

        user_dir = os.path.join(DATASET_DIR, str(user_id))
        create_dir(user_dir)

        existing = [f for f in os.listdir(user_dir) if f.endswith(".jpg")]
        next_id = len(existing)

        filename = os.path.join(user_dir, f"{next_id:04d}.jpg")
        cv2.imwrite(filename, face_crop)

        # Lưu employee metadata
        self.employee_service.add_employee(user_id)

        return filename

    def save_faces_from_video(self, video_path: str, user_id: str) -> int:
        user_dir = os.path.join(DATASET_DIR, str(user_id))
        create_dir(user_dir)

        # 🔥 FIX: lấy index hiện tại
        existing = [f for f in os.listdir(user_dir) if f.endswith(".jpg")]
        start_index = len(existing)

        cap = cv2.VideoCapture(video_path)
        count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_idx = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

            if frame_idx % 5 == 0:
                faces = self.detector.detect(frame)

                for (x, y, w, h) in faces:
                    face_crop = frame[y:y + h, x:x + w]
                    face_crop = cv2.resize(face_crop, (200, 200))

                    # 🔥 FIX: cộng offset
                    filename = os.path.join(
                        user_dir, f"{start_index + count:04d}.jpg"
                    )

                    cv2.imwrite(filename, face_crop)
                    count += 1

        cap.release()

        self.employee_service.add_employee(user_id)

        print(f"✅ Extracted {count} faces for user {user_id}")
        return count