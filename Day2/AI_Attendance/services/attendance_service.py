from datetime import datetime, timedelta, time

from db.database import AttendanceDatabase


class AttendanceService:
    """
    Service xử lý nghiệp vụ attendance:
    - Check-in / Check-out theo ca hành chính
    - Tính trạng thái đi muộn / về sớm
    - Truy vấn báo cáo theo ngày/tháng
    """

    SHIFT_START = time(8, 0, 0)
    LATE_AFTER = time(8, 0, 1)
    SHIFT_END = time(17, 0)

    def __init__(self):
        self.db = AttendanceDatabase()

    def _calc_check_in(self, dt: datetime) -> tuple[str, str]:
        """
        Tính trạng thái check-in.
        Trả về:
        - status_in: On Time | Late
        - note: ghi chú chi tiết số phút muộn
        """
        if dt.time() > self.LATE_AFTER:
            base_minutes = self.SHIFT_START.hour * 60 + self.SHIFT_START.minute
            now_minutes = dt.hour * 60 + dt.minute
            late_minutes = max(now_minutes - base_minutes, 0)
            return "Late", f"Muon {late_minutes} phut"
        return "On Time", "Dung gio"

    def _calc_check_out(self, dt: datetime) -> tuple[str, str]:
        """
        Tính trạng thái check-out.
        Trả về:
        - status_out: Normal | Early Leave
        - note: ghi chú chi tiết số phút về sớm
        """
        if dt.time() < self.SHIFT_END:
            base_minutes = self.SHIFT_END.hour * 60 + self.SHIFT_END.minute
            now_minutes = dt.hour * 60 + dt.minute
            early_minutes = max(base_minutes - now_minutes, 0)
            return "Early Leave", f"Ve som {early_minutes} phut"
        return "Normal", "Tan ca dung gio"

    def check_in(self, user_id: str, now: datetime | None = None) -> dict:
        """
        Check-in cho nhân sự.
        Rule:
        - Không cho check-in lần 2 trong cùng ngày nếu đã có bản ghi ca làm.
        """
        now = now or datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        check_in_time = now.strftime("%H:%M:%S")
        status_in, note = self._calc_check_in(now)

        with self.db.get_conn() as conn:
            row = conn.execute(
                """
                SELECT id, check_out_time
                FROM attendance_logs
                WHERE user_id = ? AND date = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (str(user_id), date_str),
            ).fetchone()

            if row is not None:
                if row["check_out_time"] is None:
                    return {
                        "success": False,
                        "message": "Nhan vien da check-in va chua check-out.",
                    }
                return {
                    "success": False,
                    "message": "Nhan vien da hoan tat ca lam trong ngay nay.",
                }

            conn.execute(
                """
                INSERT INTO attendance_logs (user_id, date, check_in_time, status_in, note)
                VALUES (?, ?, ?, ?, ?)
                """,
                (str(user_id), date_str, check_in_time, status_in, note),
            )

        return {
            "success": True,
            "message": f"Check-in thanh cong: {status_in}",
            "status_in": status_in,
            "note": note,
        }

    def check_out(self, user_id: str, now: datetime | None = None) -> dict:
        """
        Check-out cho nhân sự.
        Rule:
        - Chỉ check-out được khi đã có check-in mở trong ngày.
        """
        now = now or datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        check_out_time = now.strftime("%H:%M:%S")
        status_out, note = self._calc_check_out(now)

        with self.db.get_conn() as conn:
            row = conn.execute(
                """
                SELECT id
                FROM attendance_logs
                WHERE user_id = ? AND date = ? AND check_out_time IS NULL
                ORDER BY id DESC
                LIMIT 1
                """,
                (str(user_id), date_str),
            ).fetchone()

            if row is None:
                return {
                    "success": False,
                    "message": "Khong tim thay check-in hop le de check-out.",
                }

            conn.execute(
                """
                UPDATE attendance_logs
                SET check_out_time = ?, status_out = ?, note = CASE
                    WHEN note IS NULL OR note = '' THEN ?
                    ELSE note || '; ' || ?
                END
                WHERE id = ?
                """,
                (check_out_time, status_out, note, note, row["id"]),
            )

        return {
            "success": True,
            "message": f"Check-out thanh cong: {status_out}",
            "status_out": status_out,
            "note": note,
        }

    def get_today_stats(self, total_users: int) -> dict:
        """
        Trả về thống kê realtime ngày hiện tại:
        - Đã có mặt, Đi muộn, Vắng mặt
        """
        today = datetime.now().strftime("%Y-%m-%d")
        with self.db.get_conn() as conn:
            row = conn.execute(
                """
                SELECT
                    COUNT(DISTINCT user_id) AS present_count,
                    SUM(CASE WHEN status_in = 'Late' THEN 1 ELSE 0 END) AS late_count
                FROM attendance_logs
                WHERE date = ?
                """,
                (today,),
            ).fetchone()

        present = int(row["present_count"] or 0)
        late = int(row["late_count"] or 0)
        absent = max(total_users - present, 0)

        return {
            "present": present,
            "late": late,
            "absent": absent,
        }

    def get_weekly_attendance(self) -> dict:
        """
        Trả về số lượt check-in trong 7 ngày gần nhất cho Dashboard chart.
        """
        base = datetime.now().date()
        date_keys = []
        for i in range(6, -1, -1):
            d = base - timedelta(days=i)
            date_keys.append(d.strftime("%Y-%m-%d"))

        values_map = {d: 0 for d in date_keys}

        with self.db.get_conn() as conn:
            rows = conn.execute(
                """
                SELECT date, COUNT(*) AS total
                FROM attendance_logs
                WHERE date BETWEEN ? AND ?
                GROUP BY date
                ORDER BY date ASC
                """,
                (date_keys[0], date_keys[-1]),
            ).fetchall()

        for row in rows:
            key = row["date"]
            if key in values_map:
                values_map[key] = int(row["total"] or 0)

        labels = [datetime.strptime(k, "%Y-%m-%d").strftime("%a") for k in date_keys]
        values = [values_map[k] for k in date_keys]
        return {"labels": labels, "values": values}

    def get_monthly_report(self, user_id: str, year: int, month: int) -> dict:
        """
        Báo cáo tháng cho 1 nhân viên.
        - Summary: tổng ngày công, số đi muộn, số về sớm, punctuality
        - Details: danh sách từng ngày
        """
        start_date = f"{year:04d}-{month:02d}-01"
        if month == 12:
            end_date = f"{year + 1:04d}-01-01"
        else:
            end_date = f"{year:04d}-{month + 1:02d}-01"

        with self.db.get_conn() as conn:
            details = conn.execute(
                """
                SELECT
                    a.date,
                    a.check_in_time,
                    a.check_out_time,
                    a.status_in,
                    a.status_out,
                    a.note,
                    COALESCE(e.name, a.user_id) AS employee_name
                FROM attendance_logs a
                LEFT JOIN employee_meta e ON e.user_id = a.user_id
                WHERE a.user_id = ? AND a.date >= ? AND a.date < ?
                ORDER BY a.date ASC
                """,
                (str(user_id), start_date, end_date),
            ).fetchall()

        calc = self.calculate_attendance(user_id=user_id, year=year, month=month)
        total_workdays = calc["total_workdays"]
        total_late = calc["total_late"]
        total_early = calc["total_early"]
        punctuality = calc["punctuality"]

        detail_rows = []
        for row in details:
            detail_rows.append(
                {
                    "date": row["date"],
                    "check_in_time": row["check_in_time"] or "",
                    "check_out_time": row["check_out_time"] or "",
                    "status": self._compose_status(row["status_in"], row["status_out"]),
                    "note": row["note"] or "",
                    "employee_name": row["employee_name"] or str(user_id),
                }
            )

        return {
            "summary": {
                "total_workdays": total_workdays,
                "total_late": total_late,
                "total_early": total_early,
                "punctuality": punctuality,
            },
            "details": detail_rows,
        }

    def calculate_attendance(self, user_id: str, year: int, month: int) -> dict:
        """
        Hàm audit logic báo cáo:
        - Tổng buổi đi làm: đếm ngày duy nhất có check-in
        - Tỷ lệ chuyên cần: (ngày đúng giờ / tổng ngày đi làm) * 100
        """
        start_date = f"{year:04d}-{month:02d}-01"
        if month == 12:
            end_date = f"{year + 1:04d}-01-01"
        else:
            end_date = f"{year:04d}-{month + 1:02d}-01"

        with self.db.get_conn() as conn:
            row = conn.execute(
                """
                SELECT
                    COUNT(DISTINCT CASE WHEN check_in_time IS NOT NULL THEN date END) AS total_workdays,
                    COUNT(DISTINCT CASE WHEN status_in = 'Late' THEN date END) AS total_late,
                    COUNT(DISTINCT CASE WHEN status_out = 'Early Leave' THEN date END) AS total_early,
                    COUNT(DISTINCT CASE WHEN status_in = 'On Time' THEN date END) AS on_time_days
                FROM attendance_logs
                WHERE user_id = ? AND date >= ? AND date < ?
                """,
                (str(user_id), start_date, end_date),
            ).fetchone()

        total_workdays = int(row["total_workdays"] or 0)
        total_late = int(row["total_late"] or 0)
        total_early = int(row["total_early"] or 0)
        on_time_days = int(row["on_time_days"] or 0)

        punctuality = 0.0
        if total_workdays > 0:
            punctuality = round((on_time_days / total_workdays) * 100, 2)

        return {
            "total_workdays": total_workdays,
            "total_late": total_late,
            "total_early": total_early,
            "punctuality": punctuality,
        }

    def _compose_status(self, status_in: str | None, status_out: str | None) -> str:
        """
        Chuẩn hóa trạng thái hiển thị ở report.
        """
        in_status = status_in or "N/A"
        out_status = status_out or "Pending"
        if in_status == "On Time" and out_status == "Normal":
            return "Hop le"
        if in_status == "Late" and out_status == "Early Leave":
            return "Muon + Ve som"
        if in_status == "Late":
            return "Muon"
        if out_status == "Early Leave":
            return "Ve som"
        return f"{in_status} / {out_status}"

    def sync_employee_meta(self, employees: dict):
        """
        Đồng bộ metadata nhân sự vào SQLite để phục vụ JOIN report.
        """
        with self.db.get_conn() as conn:
            for user_id, info in employees.items():
                conn.execute(
                    """
                    INSERT INTO employee_meta (user_id, name, department)
                    VALUES (?, ?, ?)
                    ON CONFLICT(user_id) DO UPDATE SET
                        name = excluded.name,
                        department = excluded.department
                    """,
                    (
                        str(user_id),
                        info.get("name", str(user_id)),
                        info.get("department", "Unknown"),
                    ),
                )

    def delete_user_data(self, user_id: str):
        """
        Xóa toàn bộ dữ liệu attendance của user trong DB để đảm bảo toàn vẹn dữ liệu.
        """
        with self.db.get_conn() as conn:
            conn.execute("DELETE FROM attendance_logs WHERE user_id = ?", (str(user_id),))
            conn.execute("DELETE FROM employee_meta WHERE user_id = ?", (str(user_id),))
