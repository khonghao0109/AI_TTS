import json
import os

EMPLOYEE_FILE = "data/employees.json"


class EmployeeService:
    def __init__(self):
        if not os.path.exists(EMPLOYEE_FILE):
            self._save({})

    def add_employee(self, user_id, name=None, department=None, role=None, email=None, phone=None):
        data = self._load()

        if user_id not in data:
            # 🔥 Lấy avatar từ dataset
            dataset_path = f"data/dataset/{user_id}"
            avatar = ""

            if os.path.exists(dataset_path):
                files = [f for f in os.listdir(dataset_path) if f.endswith(".jpg")]
                if files:
                    avatar = os.path.join(dataset_path, files[0])

            data[user_id] = {
                "user_id": user_id,
                "name": name or f"User {user_id}",
                "department": department or "Unknown",
                "role": role or "Staff",
                "email": email or "",
                "phone": phone or "",
                "avatar": avatar  # 🔥 NEW
            }

        self._save(data)

    def update_employee(self, user_id, **kwargs):
        data = self._load()

        if user_id in data:
            for key, value in kwargs.items():
                if value:
                    data[user_id][key] = value

        self._save(data)

    def get_all(self):
        return self._load()

    def _load(self):
        try:
            with open(EMPLOYEE_FILE, "r") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except json.JSONDecodeError:
            print("⚠️ employees.json lỗi → reset")
            self._save({})
            return {}

    def _save(self, data):
        os.makedirs(os.path.dirname(EMPLOYEE_FILE), exist_ok=True)
        with open(EMPLOYEE_FILE, "w") as f:
            json.dump(data, f, indent=4)