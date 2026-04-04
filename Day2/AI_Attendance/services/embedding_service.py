from typing import Optional

import numpy as np


class EmbeddingService:
    """
    Service mẫu để tích hợp model embedding (FaceNet/InsightFace).
    Lưu ý:
    - File này là skeleton định hướng mở rộng.
    - Mặc định chưa bật inference thật để tránh thêm dependency bắt buộc.
    """

    def __init__(self):
        self.backend = None
        self._try_load_backend()

    def _try_load_backend(self):
        """
        Tự động thử nạp backend InsightFace nếu có cài đặt.
        Nếu chưa có, service vẫn khởi tạo an toàn để app không crash.
        """
        try:
            from insightface.app import FaceAnalysis  # type: ignore

            app = FaceAnalysis(name="buffalo_l")
            app.prepare(ctx_id=0, det_size=(640, 640))
            self.backend = app
        except Exception:
            self.backend = None

    def extract_embedding(self, bgr_face: np.ndarray) -> Optional[np.ndarray]:
        """
        Trích xuất vector embedding từ ảnh khuôn mặt.
        Trả về None nếu backend chưa sẵn sàng.
        """
        if self.backend is None or bgr_face is None or bgr_face.size == 0:
            return None

        faces = self.backend.get(bgr_face)
        if not faces:
            return None

        emb = faces[0].embedding.astype(np.float32)
        norm = np.linalg.norm(emb)
        if norm == 0:
            return None
        return emb / norm

    @staticmethod
    def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        """
        Tính cosine similarity giữa 2 vector embedding.
        """
        if vec_a is None or vec_b is None:
            return -1.0
        return float(np.dot(vec_a, vec_b))
