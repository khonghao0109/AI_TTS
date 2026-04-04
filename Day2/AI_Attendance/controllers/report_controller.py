from services.attendance_service import AttendanceService
from services.employee_service import EmployeeService


class ReportController:
    """Controller quản lý dữ liệu cho màn Báo cáo attendance."""

    def __init__(self):
        self.employee_service = EmployeeService()
        self.attendance_service = AttendanceService()

    def get_employee_options(self) -> list[tuple[str, str]]:
        """
        Trả về danh sách tuple (user_id, display_text) cho combobox filter.
        """
        data = self.employee_service.get_all()
        options = []
        for user_id, info in data.items():
            name = info.get("name", user_id)
            options.append((user_id, f"{name} ({user_id})"))
        return sorted(options, key=lambda x: x[1].lower())

    def get_month_report(self, user_id: str, year: int, month: int) -> dict:
        self.attendance_service.sync_employee_meta(self.employee_service.get_all())
        return self.attendance_service.get_monthly_report(
            user_id=user_id,
            year=year,
            month=month,
        )
