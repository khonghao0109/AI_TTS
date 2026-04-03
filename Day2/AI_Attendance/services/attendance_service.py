import os
from datetime import datetime
from config import ATTENDANCE_DIR
from core.utils import create_dir

class AttendanceService:
    """Service ghi chép attendance (sẵn sàng mở rộng)"""
    def __init__(self):
        create_dir(ATTENDANCE_DIR)

    def mark_attendance(self, user_id: str):
        log_file = os.path.join(ATTENDANCE_DIR, "attendance_log.csv")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(log_file, "a", encoding="utf-8") as f:
            if os.path.getsize(log_file) == 0:
                f.write("user_id,timestamp\n")
            f.write(f"{user_id},{timestamp}\n")

        return timestamp