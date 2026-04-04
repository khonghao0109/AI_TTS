import os

from config import DATASET_DIR
from services.attendance_service import AttendanceService
from services.employee_service import EmployeeService


class DashboardController:
    """Controller xử lý dữ liệu cho màn Dashboard (MVC)."""

    def __init__(self):
        self.employee_service = EmployeeService()
        self.attendance_service = AttendanceService()

    def get_summary(self) -> dict:
        employees = self.employee_service.get_all()
        total_users = len(employees)

        total_images = 0
        if os.path.exists(DATASET_DIR):
            for user_id in os.listdir(DATASET_DIR):
                folder = os.path.join(DATASET_DIR, user_id)
                if os.path.isdir(folder):
                    total_images += len(
                        [name for name in os.listdir(folder) if name.lower().endswith(".jpg")]
                    )

        return {
            "total_users": total_users,
            "total_images": total_images,
        }

    def get_weekly_attendance(self) -> dict:
        return self.attendance_service.get_weekly_attendance()

    def get_live_stats(self) -> dict:
        total_users = len(self.employee_service.get_all())
        return self.attendance_service.get_today_stats(total_users=total_users)
