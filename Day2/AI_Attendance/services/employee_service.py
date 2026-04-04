import json
import os
import shutil

from config import DATASET_DIR, EMPLOYEE_FILE
from services.attendance_service import AttendanceService


class EmployeeService:
    def __init__(self):
        if not os.path.exists(EMPLOYEE_FILE):
            self._save({})
        self._cache_data: dict | None = None
        self._cache_stamp: tuple[int, int] | None = None
        self.attendance_service = AttendanceService()

    def add_employee(self, user_id, name=None, department=None, role=None, email=None, phone=None):
        user_id = str(user_id)
        data = self._load()

        if user_id not in data:
            dataset_path = os.path.join(DATASET_DIR, user_id)
            avatar = ""

            if os.path.exists(dataset_path):
                files = sorted([f for f in os.listdir(dataset_path) if f.lower().endswith(".jpg")])
                if files:
                    avatar = os.path.join(dataset_path, files[0])

            data[user_id] = {
                "user_id": user_id,
                "name": name or f"User {user_id}",
                "department": department or "Unknown",
                "role": role or "Staff",
                "email": email or "",
                "phone": phone or "",
                "avatar": avatar,
            }

        self._save(data)

    def update_employee(self, user_id, **kwargs):
        user_id = str(user_id)
        data = self._load()

        if user_id in data:
            for key, value in kwargs.items():
                if value is not None and value != "":
                    data[user_id][key] = value

        self._save(data)

    def delete_employee(self, user_id: str) -> dict:
        """
        Xóa nhân sự triệt để:
        1) Xóa bản ghi user trong employee store
        2) Xóa dữ liệu attendance liên quan trong DB
        3) Xóa folder ảnh dataset của user
        """
        user_id = str(user_id)
        data = self._load()
        existed = user_id in data

        if user_id in data:
            del data[user_id]
            self._save(data)

        # Bước 1: dọn dữ liệu DB attendance/report
        self.attendance_service.delete_user_data(user_id)

        # Bước 2: dọn toàn bộ ảnh dataset của nhân sự
        user_dataset_path = os.path.join(DATASET_DIR, user_id)
        folder_removed = False
        if os.path.isdir(user_dataset_path):
            shutil.rmtree(user_dataset_path, ignore_errors=True)
            folder_removed = True

        return {
            "success": existed or folder_removed,
            "user_id": user_id,
            "folder_removed": folder_removed,
        }

    def get_all(self):
        return self._load()

    def get_departments(self) -> list[str]:
        data = self._load()
        departments = sorted(
            {info.get("department", "Unknown") for info in data.values() if info.get("department", "")}
        )
        return departments

    def search_and_filter(self, keyword: str = "", department: str = "All") -> dict:
        """
        Tối ưu query theo hướng in-memory index:
        - Dữ liệu chỉ đọc 1 lần (cache theo mtime file)
        - Search trên các cột phổ biến
        """
        keyword_norm = (keyword or "").strip().lower()
        data = self._load()
        result = {}

        for user_id, info in data.items():
            if department and department != "All":
                if info.get("department", "") != department:
                    continue

            if keyword_norm:
                haystack = " ".join(
                    [
                        user_id,
                        info.get("name", ""),
                        info.get("department", ""),
                        info.get("role", ""),
                        info.get("email", ""),
                        info.get("phone", ""),
                    ]
                ).lower()
                if keyword_norm not in haystack:
                    continue

            result[user_id] = info

        return result

    def _load(self):
        if os.path.exists(EMPLOYEE_FILE):
            stat = os.stat(EMPLOYEE_FILE)
            stamp = (int(stat.st_mtime_ns), int(stat.st_size))
        else:
            stamp = (0, 0)

        if self._cache_data is not None and self._cache_stamp == stamp:
            return dict(self._cache_data)

        try:
            with open(EMPLOYEE_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    self._cache_data = {}
                    self._cache_stamp = stamp
                    return {}
                data = json.loads(content)
                self._cache_data = data
                self._cache_stamp = stamp
                return dict(data)
        except json.JSONDecodeError:
            self._save({})
            return {}

    def _save(self, data):
        os.makedirs(os.path.dirname(EMPLOYEE_FILE), exist_ok=True)

        # Ghi file atomic để tránh lỗi dữ liệu khi app bị tắt đột ngột.
        temp_path = EMPLOYEE_FILE + ".tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        os.replace(temp_path, EMPLOYEE_FILE)

        self._cache_data = dict(data)
        stat = os.stat(EMPLOYEE_FILE)
        self._cache_stamp = (int(stat.st_mtime_ns), int(stat.st_size))
