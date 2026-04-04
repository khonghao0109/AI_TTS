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

## 🆕 Cập nhật nâng cao Day 2 (UI + Logic + Database)

### 1. UI/UX nâng cấp (Dark Mode + Responsive)

- Áp dụng theme tối hiện đại bằng QSS (font ưu tiên: Montserrat/Roboto)
- Sidebar dạng slim có icon, tự mở rộng khi hover
- Dashboard cân đối bằng `QGridLayout`:
  - Hàng 1: 4 card chỉ số ngang đều nhau
  - Hàng 2: biểu đồ attendance (70%) + widget thông báo nhanh (30%)
- Căn chỉnh chuẩn responsive:
  - `setContentsMargins(20, 20, 20, 20)`
  - `setSpacing(15)`
  - `setRowStretch(0, 1)` và `setRowStretch(1, 2)`

### 2. Attendance Business Logic chuẩn ca làm

- Ca hành chính: `08:00 - 17:00`
- `Late` khi check-in `> 08:00:01`
- `Early Leave` khi check-out `< 17:00:00`
- Validation:
  - Không cho check-in 2 lần khi chưa check-out
  - Check-out chỉ hợp lệ khi đã có check-in mở trong ngày

### 3. Database hóa dữ liệu attendance (SQLite)

- Bổ sung schema `attendance_logs`:
  - `user_id, date, check_in_time, check_out_time, status_in, status_out, note`
- Bổ sung index tối ưu truy vấn tháng/ngày
- Đồng bộ `employee_meta` để phục vụ report bằng `JOIN`

### 4. Trang Báo cáo (Report Tab)

- Filter theo nhân sự + tháng + năm
- Summary card:
  - Tổng ngày công thực tế (ngày duy nhất có check-in)
  - Tổng số lần đi muộn
  - Tổng số lần về sớm
  - Tỷ lệ chuyên cần `%`
- Bảng lịch sử chi tiết:
  - Ngày, Giờ vào, Giờ ra, Trạng thái, Ghi chú

### 5. Xóa nhân sự triệt để + Auto Retrain

- Khi xóa nhân sự:
  1. Xóa dữ liệu nhân sự và attendance trong DB
  2. Xóa toàn bộ thư mục ảnh dataset theo `user_id` bằng `shutil.rmtree`
  3. Tự động train lại model
- Quá trình retrain chạy trong `QThread` riêng để UI không bị treo
- Trước khi train, hệ thống tự xóa model cũ (`.yml/.h5/.xml/...`) để tránh stale model

### 6. Tối ưu camera thread và đồng bộ UI

- Sửa lỗi worker bị xóa khi đang emit frame (`CameraWorker deleted`)
- Chuyển lệnh collect/train sang cơ chế command queue nội bộ worker
- Đồng bộ realtime:
  - Sau collect/train thành công, tab Nhân sự và Dashboard tự refresh
  - Không cần tắt/mở lại app để thấy nhân sự mới

---

## ⚠️ Hạn chế hiện tại Day 2

- LBPH phù hợp local/offline nhưng độ chính xác còn hạn chế ở môi trường phức tạp
- Chưa có anti-spoof/liveness detection
- Chưa triển khai phân quyền người dùng (admin/staff)

---

## 🚀 Hướng phát triển Day 2

- Nâng cấp nhận diện sang embedding model (FaceNet/InsightFace)
- Bổ sung liveness detection để chống giả mạo
- Thêm export báo cáo (CSV/Excel/PDF)
- Tích hợp thông báo check-in/check-out theo thời gian thực (toast/desktop notification)

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

# 🚀 NGÀY 4 – FASTAPI (THE MODERN API)

## 🎯 MỤC TIÊU

- Xây dựng REST API hoàn chỉnh
- Hiểu cơ chế hoạt động HTTP
- Validate dữ liệu với Pydantic
- Làm việc với:
  - Path params
  - Query params
  - Headers
  - Cookies
- Áp dụng Middleware (production mindset)
- Hoàn thành CRUD cho ứng dụng Blog

## 🏗️ CẤU TRÚC PROJECT

```text
Day4/
│
├── src/
│   ├── main.py              ← Entry point (FastAPI app)
│   │
│   ├── api/
│   │   └── posts.py         ← Router (HTTP layer)
│   │
│   ├── schemas/
│   │   └── post.py          ← Pydantic models
│   │
│   ├── services/
│   │   └── post_service.py  ← Business logic
│   │
│   ├── core/                ← (reserved)
│   └── db/                  ← (Day 5)
│
└── tests/
```

## 🧠 KIẾN TRÚC

```text
Client → Router → Service → Storage (RAM)
               ↓
           Pydantic
```

## 🧠 KIẾN THỨC CỐT LÕI

### 1. FastAPI – Routing

```python
@app.get("/posts")
@app.post("/posts")
@app.put("/posts/{id}")
@app.delete("/posts/{id}")
```

👉 Mapping HTTP → function

### 2. Pydantic – Data Validation

```python
class PostCreate(BaseModel):
    title: str = Field(..., min_length=3)
    content: str
```

👉 Tự động:

- Validate request
- Parse JSON → object
- Trả lỗi 422 nếu sai

### 3. Response Model (Contract API)

```python
@router.post("/posts", response_model=Post)
```

👉 Đảm bảo output đúng schema

### 4. CRUD Operations

- ✔ Create: `POST /posts`
- ✔ Read: `GET /posts`, `GET /posts/{id}`
- ✔ Update: `PUT /posts/{id}`
- ✔ Delete: `DELETE /posts/{id}`

### 5. HTTP Status Code

| Code | Ý nghĩa          |
| ---- | ---------------- |
| 200  | OK               |
| 201  | Created          |
| 204  | No Content       |
| 404  | Not Found        |
| 422  | Validation Error |

## 🔍 CÁC KỸ THUẬT QUAN TRỌNG

### 6. Path Parameter

```python
post_id: int = Path(..., gt=0)
```

👉 Validate ngay tại router

### 7. Query Parameter

`GET /posts?keyword=python`

👉 Filter data tại service:

```python
keyword in post.title.lower()
```

### 8. Header (Request Tracking)

Input:

```python
x_request_id: str | None = Header(...)
```

### 9. Middleware (Production Pattern)

```python
@app.middleware("http")
```

👉 Dùng để:

- Logging
- Authentication
- Tracing

### 10. Cookie

```python
user_session: str | None = Cookie(...)
```

👉 Phân biệt:

- Có cookie → user = session
- Không → user = guest

## 🧪 QUÁ TRÌNH TEST (POSTMAN)

- ✔ Test 1 – Health Check: `GET /` → API running
- ✔ Test 2 – Create Post: `POST /posts`
  - Fix lỗi: `422` do gửi sai Body (Params vs JSON)
- ✔ Test 3 – Get All: `GET /posts`
- ✔ Test 4 – Get By ID: `GET /posts/1`
- ✔ Test 5 – Update: `PUT /posts/1` (verify bằng GET lại)
- ✔ Test 6 – Delete: `DELETE /posts/1` → `204`, không có body
- ✔ Test 7 – Query Param: `GET /posts?keyword=python`
- ✔ Test 8 – Header: `X-Request-ID: test-123` → log + response header
- ✔ Test 9 – Cookie: `Cookie: user_session=abc123`
  - Fix lỗi: Invalid header format
  - Dùng Cookie Manager

## ⚠️ BUG & BÀI HỌC

### ❌ 1. ModuleNotFoundError

→ Sai cách chạy (`python main.py`)

✔ Fix:

```bash
poetry run uvicorn src.main:app --reload
```

### ❌ 2. 422 Validation Error

→ Gửi sai body

✔ Fix:

- Chọn Body → raw → JSON

### ❌ 3. Cookie header lỗi

→ Format sai

✔ Fix:

- Dùng Cookie Manager

### ❌ 4. Data mất sau restart

👉 Vì storage = RAM

## 🧠 INSIGHT QUAN TRỌNG

1. Separation of Concerns: API → Service → Storage
2. Stateless API: Server không giữ state
3. Contract-first design: Schema = hợp đồng
4. Middleware = cross-cutting concern
5. In-memory chỉ là tạm thời

👉 Chuẩn production: Database (Day 5)

## 🎯 KẾT QUẢ ĐẠT ĐƯỢC

- ✔ Xây dựng API hoàn chỉnh
- ✔ Hiểu HTTP lifecycle
- ✔ Validate dữ liệu chuẩn
- ✔ Xử lý lỗi đúng chuẩn REST
- ✔ Biết debug thực tế
- ✔ Làm chủ Postman
- ✔ Hiểu rõ flow backend

# 📌 KẾT LUẬN SAU 4 NGÀY

- ✔ Hiểu về nền tảng Python, xử lý file và OpenCV
- ✔ Xây dựng hệ thống AI Attendance có cấu trúc rõ ràng
- ✔ Làm việc được với Database và ETL pipeline theo hướng chuẩn hóa
- ✔ Xây dựng REST API hoàn chỉnh bằng FastAPI (CRUD, validation, middleware)
- ✔ Hiểu và áp dụng các thành phần HTTP quan trọng: path/query/header/cookie
- ✔ Hình thành tư duy backend thực chiến: tách layer, contract-first, observability cơ bản
