# config hệ thống

import os

# Base directory của project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Thư mục dữ liệu
DATA_DIR = os.path.join(BASE_DIR, "data")
DATASET_DIR = os.path.join(DATA_DIR, "dataset")
ATTENDANCE_DIR = os.path.join(DATA_DIR, "attendance")
MODELS_DIR = os.path.join(BASE_DIR, "models")   

# Assets
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
HAARCASCADE_PATH = os.path.join(ASSETS_DIR, "haarcascade_frontalface_default.xml")