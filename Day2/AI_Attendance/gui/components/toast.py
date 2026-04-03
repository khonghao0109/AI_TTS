# gui/components/toast.py
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QTimer

class Toast(QLabel):
    def __init__(self, parent, message):
        super().__init__(parent)
        self.setText(message)
        self.setStyleSheet("background: green; color: white; padding: 10px;")
        self.move(800, 50)
        self.show()

        QTimer.singleShot(2000, self.close)