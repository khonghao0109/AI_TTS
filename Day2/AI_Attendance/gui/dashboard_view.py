from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import os

from config import DATASET_DIR
from services.employee_service import EmployeeService


class DashboardView(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout(self)
        self.layout.setSpacing(20)

        self.card_users = self.create_card("Users", "0")
        self.card_images = self.create_card("Images", "0")

        self.layout.addWidget(self.card_users, 0, 0)
        self.layout.addWidget(self.card_images, 0, 1)

        self.refresh()

    def create_card(self, title, value):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: #2c3e50;
                color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)

        layout = QVBoxLayout(card)

        label_title = QLabel(title)
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setStyleSheet("font-size: 16px;")

        label_value = QLabel(value)
        label_value.setAlignment(Qt.AlignCenter)
        label_value.setStyleSheet("font-size: 28px; font-weight: bold;")

        layout.addWidget(label_title)
        layout.addWidget(label_value)

        card.label_value = label_value
        return card

    def refresh(self):
        service = EmployeeService()
        employees = service.get_all()

        total_users = len(employees)

        total_images = 0
        for user_id in os.listdir(DATASET_DIR):
            path = os.path.join(DATASET_DIR, user_id)
            if os.path.isdir(path):
                total_images += len(os.listdir(path))

        self.card_users.label_value.setText(str(total_users))
        self.card_images.label_value.setText(str(total_images))