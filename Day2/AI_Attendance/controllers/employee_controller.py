from services.employee_service import EmployeeService


class EmployeeController:
    """Controller cho màn Nhân sự, tách business logic khỏi view."""

    def __init__(self):
        self.employee_service = EmployeeService()

    def get_employees(self, keyword: str = "", department: str = "All") -> dict:
        return self.employee_service.search_and_filter(
            keyword=keyword,
            department=department,
        )

    def get_departments(self) -> list[str]:
        return self.employee_service.get_departments()

    def add_employee(self, user_id: str, **kwargs):
        self.employee_service.add_employee(user_id, **kwargs)

    def update_employee(self, user_id: str, **kwargs):
        self.employee_service.update_employee(user_id, **kwargs)

    def delete_employee(self, user_id: str) -> dict:
        return self.employee_service.delete_employee(user_id)
