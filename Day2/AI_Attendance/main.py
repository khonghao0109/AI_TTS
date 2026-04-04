import sys

from PyQt5.QtWidgets import QApplication

from config import ASSETS_DIR, ATTENDANCE_DIR, DATASET_DIR, MODEL_DATA_DIR
from core.utils import create_dir
from gui.main_window import MainWindow


if __name__ == "__main__":
    # Ensure required directories exist
    for path in [DATASET_DIR, ATTENDANCE_DIR, MODEL_DATA_DIR, ASSETS_DIR]:
        create_dir(path)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
