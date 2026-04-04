import os
import sqlite3
from contextlib import contextmanager

from config import ATTENDANCE_DB_PATH
from core.utils import create_dir


class AttendanceDatabase:
    """Lớp quản lý kết nối SQLite cho module attendance."""

    def __init__(self):
        create_dir(os.path.dirname(ATTENDANCE_DB_PATH))
        self.db_path = ATTENDANCE_DB_PATH
        self.init_schema()

    @contextmanager
    def get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_schema(self):
        """Khởi tạo schema chuẩn cho attendance logs và index tối ưu truy vấn."""
        with self.get_conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS attendance_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    check_in_time TEXT,
                    check_out_time TEXT,
                    status_in TEXT,
                    status_out TEXT,
                    note TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_attendance_user_date
                ON attendance_logs (user_id, date)
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_attendance_date
                ON attendance_logs (date)
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS employee_meta (
                    user_id TEXT PRIMARY KEY,
                    name TEXT,
                    department TEXT
                )
                """
            )
