"""Project configuration constants."""

import os

# Base directory of project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data directories
DATA_DIR = os.path.join(BASE_DIR, "data")
DATASET_DIR = os.path.join(DATA_DIR, "dataset")
ATTENDANCE_DIR = os.path.join(DATA_DIR, "attendance")
ATTENDANCE_DB_PATH = os.path.join(ATTENDANCE_DIR, "attendance.db")
MODEL_DATA_DIR = os.path.join(DATA_DIR, "models")

# Canonical model paths
FACE_MODEL_PATH = os.path.join(MODEL_DATA_DIR, "face_model.yml")
LABELS_PATH = os.path.join(MODEL_DATA_DIR, "labels.json")
EMPLOYEE_FILE = os.path.join(DATA_DIR, "employees.json")

# Assets
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
HAARCASCADE_PATH = os.path.join(ASSETS_DIR, "haarcascade_frontalface_default.xml")
