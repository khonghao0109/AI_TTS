import os

from PyQt5.QtCore import QObject, QThread, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPainterPath, QPixmap
from PyQt5.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QStyle,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from controllers.employee_controller import EmployeeController
from core.face_recognizer import FaceRecognizer


class RetrainWorker(QObject):
    """
    Worker train model chạy nền.
    Dùng cho auto-retrain sau khi xóa nhân sự để không block UI.
    """

    finished = pyqtSignal(bool)
    error = pyqtSignal(str)

    def run(self):
        try:
            recognizer = FaceRecognizer()
            ok = recognizer.train()
            self.finished.emit(ok)
        except Exception as exc:
            self.error.emit(str(exc))


class EmployeeView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = EmployeeController()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        title = QLabel("Nhan su")
        title.setStyleSheet("font-size: 22px; font-weight: 700;")
        root.addWidget(title)

        toolbar = QFrame()
        toolbar.setObjectName("Card")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(12, 10, 12, 10)
        toolbar_layout.setSpacing(8)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tim theo ten, user id, email...")

        self.filter_department = QComboBox()
        self.filter_department.addItem("All")

        self.btn_add = QPushButton("Add")
        self.btn_add.setObjectName("PrimaryButton")
        self.btn_add.setIcon(self.style().standardIcon(QStyle.SP_FileDialogNewFolder))

        self.btn_edit = QPushButton("Edit")
        self.btn_edit.setObjectName("GhostButton")
        self.btn_edit.setIcon(self.style().standardIcon(QStyle.SP_FileDialogContentsView))

        self.btn_delete = QPushButton("Delete")
        self.btn_delete.setObjectName("GhostButton")
        self.btn_delete.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #94A3B8;")

        toolbar_layout.addWidget(self.search_input, 2)
        toolbar_layout.addWidget(self.filter_department, 1)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.btn_add)
        toolbar_layout.addWidget(self.btn_edit)
        toolbar_layout.addWidget(self.btn_delete)
        toolbar_layout.addWidget(self.status_label)

        root.addWidget(toolbar)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["Avatar", "User ID", "Name", "Department", "Role", "Email", "Phone"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(
            "QTableWidget { alternate-background-color: #0B1220; }"
            "QTableWidget::item { padding: 6px; }"
        )

        root.addWidget(self.table, stretch=1)

        self.search_input.textChanged.connect(self.reload_data)
        self.filter_department.currentTextChanged.connect(self.reload_data)
        self.btn_add.clicked.connect(self.add_employee)
        self.btn_edit.clicked.connect(self.edit_employee)
        self.btn_delete.clicked.connect(self.on_delete_button_clicked)

        self.refresh_department_filter()
        self.reload_data()

    def refresh_department_filter(self):
        departments = self.controller.get_departments()

        current = self.filter_department.currentText()
        self.filter_department.blockSignals(True)
        self.filter_department.clear()
        self.filter_department.addItem("All")
        self.filter_department.addItems(departments)

        idx = self.filter_department.findText(current)
        if idx >= 0:
            self.filter_department.setCurrentIndex(idx)
        self.filter_department.blockSignals(False)

    def _create_round_avatar(self, avatar_path: str, size: int = 40) -> QLabel:
        label = QLabel()
        label.setFixedSize(size, size)
        label.setAlignment(Qt.AlignCenter)

        if not avatar_path or not os.path.exists(avatar_path):
            label.setStyleSheet(
                "background: #1E293B; color: #94A3B8; border-radius: 20px; font-weight: 700;"
            )
            label.setText("NA")
            return label

        src = QPixmap(avatar_path)
        src = src.scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        rounded = QPixmap(size, size)
        rounded.fill(Qt.transparent)

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, src)
        painter.end()

        label.setPixmap(rounded)
        return label

    def reload_data(self):
        keyword = self.search_input.text().strip()
        department = self.filter_department.currentText()

        data = self.controller.get_employees(keyword=keyword, department=department)

        self.table.setRowCount(0)

        for row_idx, (user_id, info) in enumerate(data.items()):
            self.table.insertRow(row_idx)

            avatar_path = info.get("avatar", "")
            self.table.setCellWidget(row_idx, 0, self._create_round_avatar(avatar_path))

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
        item = self.table.item(row, 1)
        return item.text() if item else None

    def add_employee(self):
        user_id, ok = QInputDialog.getText(self, "Add", "User ID:")
        if not ok or not user_id.strip():
            return

        name, _ = QInputDialog.getText(self, "Add", "Name:")
        dept, _ = QInputDialog.getText(self, "Add", "Department:")
        role, _ = QInputDialog.getText(self, "Add", "Role:")
        email, _ = QInputDialog.getText(self, "Add", "Email:")
        phone, _ = QInputDialog.getText(self, "Add", "Phone:")

        self.controller.add_employee(
            user_id.strip(),
            name=name,
            department=dept,
            role=role,
            email=email,
            phone=phone,
        )

        self.refresh_department_filter()
        self.reload_data()

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

        self.controller.update_employee(
            user_id,
            name=name,
            department=dept,
            role=role,
            email=email,
            phone=phone,
        )

        self.refresh_department_filter()
        self.reload_data()

    def on_delete_button_clicked(self):
        """
        Sự kiện xóa nhân sự hoàn chỉnh:
        1) Xóa DB
        2) Xóa folder ảnh dataset
        3) Tự động train lại model ở background thread
        """
        user_id = self.get_selected_user()
        if not user_id:
            QMessageBox.warning(self, "Error", "Select a user")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm",
            f"Delete employee {user_id}?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return

        result = self.controller.delete_employee(user_id)
        self.refresh_department_filter()
        self.reload_data()
        self.status_label.setText(f"Deleted {result['user_id']}. Auto retrain...")
        self.train_model_async()

    def train_model_async(self):
        """
        Khởi chạy quá trình train model ở QThread riêng.
        """
        self.btn_delete.setEnabled(False)
        self.btn_add.setEnabled(False)
        self.btn_edit.setEnabled(False)

        self.train_thread = QThread(self)
        self.train_worker = RetrainWorker()
        self.train_worker.moveToThread(self.train_thread)

        self.train_thread.started.connect(self.train_worker.run)
        self.train_worker.finished.connect(self._on_retrain_finished)
        self.train_worker.error.connect(self._on_retrain_error)
        self.train_worker.finished.connect(self.train_thread.quit)
        self.train_worker.error.connect(self.train_thread.quit)
        self.train_thread.finished.connect(self.train_worker.deleteLater)
        self.train_thread.finished.connect(self.train_thread.deleteLater)
        self.train_thread.start()

    def _on_retrain_finished(self, ok: bool):
        self.btn_delete.setEnabled(True)
        self.btn_add.setEnabled(True)
        self.btn_edit.setEnabled(True)
        if ok:
            self.status_label.setText("Retrain thanh cong")
            QMessageBox.information(self, "OK", "Da xoa va train lai model thanh cong.")
        else:
            self.status_label.setText("Retrain fail (thieu data)")
            QMessageBox.warning(self, "Warning", "Da xoa user, nhung train that bai (co the thieu du data).")

    def _on_retrain_error(self, message: str):
        self.btn_delete.setEnabled(True)
        self.btn_add.setEnabled(True)
        self.btn_edit.setEnabled(True)
        self.status_label.setText("Retrain error")
        QMessageBox.warning(self, "Retrain Error", message)
