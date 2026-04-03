import sys
import os
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

if __name__ == "__main__":
    # Tạo folder cần thiết
    os.makedirs("data/dataset", exist_ok=True)
    os.makedirs("data/attendance", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    os.makedirs("assets", exist_ok=True)

    print("🚀 AI Camera Attendance System với Face Recognition")
    print("   1. Nhập User ID → Capture Face (nhiều lần)")
    print("   2. Nhấn Train Model")
    print("   3. Nhận diện tự động + lưu attendance")

    # ⚠️ BẮT BUỘC với PyQt
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())