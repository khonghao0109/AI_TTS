import cv2

class Camera:
    """Quản lý webcam"""
    def __init__(self, camera_id: int = 0):
        self.cap = cv2.VideoCapture(camera_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        if not self.cap.isOpened():
            raise RuntimeError("❌ Không thể mở camera!")

    def get_frame(self):
        """Trả về frame hiện tại"""
        ret, frame = self.cap.read()
        return frame if ret else None

    def release(self):
        """Giải phóng camera"""
        if self.cap.isOpened():
            self.cap.release()