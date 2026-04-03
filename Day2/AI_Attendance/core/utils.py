import os
import urllib.request

def ensure_haarcascade(path: str):
    """Tự động tải Haar Cascade nếu chưa có"""
    if os.path.exists(path):
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    print("🔽 Đang tải haarcascade_frontalface_default.xml...")
    urllib.request.urlretrieve(url, path)
    print("✅ Đã tải xong Haar Cascade!")

def create_dir(path: str):
    """Tạo thư mục nếu chưa tồn tại"""
    os.makedirs(path, exist_ok=True)