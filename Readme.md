# 📘 AI Attendance System – Báo cáo Thực tập

---

# 🚀 NGÀY 1 – NỀN TẢNG PYTHON + CAMERA

## 🎯 Mục tiêu

- Làm quen Python cơ bản
- Làm việc với file
- Sử dụng OpenCV
- Capture dữ liệu ảnh

---

## ✅ Bài 1 – Python cơ bản

### Yêu cầu:

- Nhập danh sách 5 sinh viên
- In ra danh sách

### Kiến thức:

- list
- input()
- loop

---

## ✅ Bài 2 – Lưu dữ liệu

### Yêu cầu:

- Nhập tên + thời gian
- Lưu vào file attendance.txt

### Kiến thức:

- File handling
- String format

---

## ✅ Bài 3 – Đọc file

### Yêu cầu:

- Đọc file attendance.txt
- In dữ liệu
- Đếm số lần chấm công

### Kiến thức:

- Read file
- Loop

---

## ✅ Bài 4 – Mở camera

### Yêu cầu:

- Mở webcam
- Hiển thị realtime
- ESC để thoát

### Kiến thức:

- OpenCV
- Video stream

---

## ✅ Bài 5 – Chụp ảnh

### Yêu cầu:

- Nhấn 's' để chụp ảnh
- Lưu vào dataset/

### Kiến thức:

- Keyboard event
- cv2.imwrite()

---

## 🎯 Kết quả ngày 1

✔ Hiểu Python cơ bản
✔ Làm việc với file
✔ Mở camera
✔ Capture dữ liệu

---

# 🚀 NGÀY 2 – XÂY DỰNG HỆ THỐNG AI

## 🎯 Mục tiêu

- Detect khuôn mặt realtime
- Lưu dataset chuẩn
- Xây dựng GUI
- Tổ chức project chuyên nghiệp
- Hiểu data flow

---

## 🏗️ Cấu trúc Project

```
AI_Attendance/
│
├── core/
│   ├── camera.py
│   ├── face_detector.py
│   ├── face_recognizer.py
│   ├── utils.py
│
├── services/
│   ├── attendance_service.py
│   ├── dataset_service.py
│   ├── employee_service.py
│   ├── recognition_service.py
│   ├── training_service.py
│
├── gui/
│   ├── main_window.py
│   ├── sidebar.py
│   ├── camera_view.py
│   ├── dashboard_view.py
│   ├── employee_view.py
│   └── components/
│       └── toast.py
│
├── data/
│   ├── dataset/
│   └── attendance/
│
├── models/
│   └── face_model.yml
│
├── assets/
│   └── haarcascade_frontalface_default.xml
│
├── config.py
├── main.py
├── test.py
└── README.md
```

---

## 🧠 Kiến trúc hệ thống

### 1. core/

- Xử lý AI (detect + recognize)

### 2. services/

- Xử lý logic (attendance, training...)

### 3. gui/

- Giao diện người dùng

### 4. data/

- Lưu trữ dữ liệu

---

## 🔄 Data Flow

```
Camera → Detect → Recognize → Attendance → Save file
```

---

## 🎯 Kết quả đạt được ngày 2

✔ Detect khuôn mặt realtime
✔ Nhận diện khuôn mặt
✔ Lưu attendance
✔ Xây dựng GUI
✔ Tổ chức project chuẩn

---

## ⚠️ Hạn chế

- Chưa dùng database
- Chưa tối ưu hiệu năng
- UI có thể lag (chưa dùng thread)

---

## 🚀 Hướng phát triển

- Thêm SQLite/MySQL
- Dùng QThread (tối ưu UI)
- Deploy app
- Mở rộng thành Web App

---

# 🚀 NGÀY 3 – ETL PIPELINE + DATABASE

## 🎯 Mục tiêu

- Quản lý môi trường bằng Poetry
- Làm việc với Database (SQLite)
- Hiểu SQLAlchemy Core
- Xây dựng ETL Pipeline
- Đảm bảo dữ liệu không bị duplicate

---

## 🏗️ Cấu trúc Project

```
day3-etl-pipeline/
│
├── src/
│   ├── config.py
│   ├── fetcher.py
│   ├── transformer.py
│   ├── database.py
│   └── loader.py
│
├── data/
│   └── books.db
│
├── main.py
├── check_db.py
├── pyproject.toml
└── poetry.lock
```

---

## 🧠 Kiến trúc hệ thống

### 1. fetcher.py (Extract)

- Gọi API Open Library
- Sử dụng `httpx`
- Có timeout + error handling

---

### 2. transformer.py (Transform)

- Làm sạch dữ liệu
- Chuẩn hóa dữ liệu

### Xử lý:

- Bỏ record thiếu `title` hoặc `work_key`
- Convert author list → string
- Normalize publish_year

---

### 3. database.py (Schema)

#### Bảng books:

| Column       | Mô tả       |
| ------------ | ----------- |
| id           | Primary Key |
| title        | NOT NULL    |
| author       | nullable    |
| publish_year | index       |
| work_key     | UNIQUE      |

---

### 4. loader.py (Load)

- Insert dữ liệu vào DB
- Dùng:

```
INSERT OR IGNORE
```

→ tránh duplicate

- Sử dụng:

```
with engine.begin()
```

---

### 5. main.py

Luồng:

```
Fetch → Transform → Load
```

---

## 🔄 Data Flow

```
API → Fetcher → Transformer → Loader → Database
```

---

## 🧪 Testing

### Chạy pipeline

```
poetry run python main.py
```

#### Kết quả:

- Lần 1:

```
Inserted > 0
```

- Lần 2:

```
Inserted = 0
```

→ Không duplicate

---

## 🧠 Kiến thức quan trọng

### 1. Poetry

- Quản lý dependency
- Đảm bảo môi trường giống nhau

---

### 2. SQLAlchemy Core

- Làm việc trực tiếp với DB
- Không phụ thuộc ORM

---

### 3. Schema-first

- Thiết kế DB trước
- Không lưu JSON bừa bãi

---

### 4. Idempotent Pipeline

```
Run nhiều lần → không duplicate
```

---

### 5. Context Manager

```
with engine.begin()
```

→ auto commit / rollback

---

## 🎯 Kết quả ngày 3

✔ Xây dựng ETL pipeline hoàn chỉnh
✔ Làm việc với database thực tế
✔ Không duplicate dữ liệu
✔ Code theo kiến trúc rõ ràng

---

## ⚠️ Hạn chế

- Chưa có logging chuyên nghiệp
- Chưa có unit test
- Chưa tối ưu async

---

## 🚀 Hướng phát triển

- PostgreSQL
- Async pipeline
- Logging + Monitoring
- Airflow / Scheduler

---

# 📌 KẾT LUẬN

Sau 3 ngày:

✔ Nắm vững Python + OpenCV
✔ Xây dựng hệ thống AI cơ bản
✔ Làm việc với Database
✔ Xây dựng ETL pipeline chuẩn
✔ Có tư duy backend / data engineer

👉 Sẵn sàng nâng cấp lên level cao hơn (Async, Performance, System Design)
