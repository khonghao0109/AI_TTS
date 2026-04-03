import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from services.employee_service import EmployeeService


class EmployeeView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Avatar", "User ID", "Name", "Department", "Role", "Email", "Phone"
        ])

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.table)

        btn_edit = QPushButton("Edit")
        btn_edit.clicked.connect(self.edit_employee)
        layout.addWidget(btn_edit)

        self.reload_data()

    def reload_data(self):
        service = EmployeeService()
        data = service.get_all()

        self.table.setRowCount(0)

        for row_idx, (user_id, info) in enumerate(data.items()):
            self.table.insertRow(row_idx)

            # ===== AVATAR =====
            avatar_path = info.get("avatar", "")

            label = QLabel()
            label.setFixedSize(60, 60)

            if avatar_path and os.path.exists(avatar_path):
                pixmap = QPixmap(avatar_path)
                label.setPixmap(
                    pixmap.scaled(60, 60, Qt.KeepAspectRatio)
                )

            self.table.setCellWidget(row_idx, 0, label)

            # ===== DATA =====
            self.table.setItem(row_idx, 1, QTableWidgetItem(user_id))
            self.table.setItem(row_idx, 2, QTableWidgetItem(info.get("name", "")))
            self.table.setItem(row_idx, 3, QTableWidgetItem(info.get("department", "")))
            self.table.setItem(row_idx, 4, QTableWidgetItem(info.get("role", "")))
            self.table.setItem(row_idx, 5, QTableWidgetItem(info.get("email", "")))
            self.table.setItem(row_idx, 6, QTableWidgetItem(info.get("phone", "")))

    def get_selected_user(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        return self.table.item(row, 1).text()  # ⚠️ sửa index (cột 1 là user_id)

    def edit_employee(self):
        user_id = self.get_selected_user()
        if not user_id:
            QMessageBox.warning(self, "Error", "Select a user")
            return

        name, _ = QInputDialog.getText(self, "Edit", "Name:")
        dept, _ = QInputDialog.getText(self, "Edit", "Department:")
        role, _ = QInputDialog.getText(self, "Edit", "Role:")
        email, _ = QInputDialog.getText(self, "Edit", "Email:")
        phone, _ = QInputDialog.getText(self, "Edit", "Phone:")

        service = EmployeeService()
        service.update_employee(
            user_id,
            name=name,
            department=dept,
            role=role,
            email=email,
            phone=phone
        )

        self.reload_data()