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

## 🗺️ Sơ đồ Draw.io Day 2

- [Day2 Architecture](Day2/diagrams/day2-architecture.drawio)
- [Day2 Camera Attendance Flow](Day2/diagrams/day2-camera-attendance-flow.drawio)
- [Day2 Delete + Retrain Flow](Day2/diagrams/day2-delete-retrain-flow.drawio)
- [Day2 Report Flow](Day2/diagrams/day2-report-flow.drawio)

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

## 🗺️ Sơ đồ Draw.io Day 3

- [Day3 Architecture](Day3/diagrams/day3-architecture.drawio)
- [Day3 ETL Runtime Flow](Day3/diagrams/day3-etl-runtime-flow.drawio)
- [Day3 DB Schema](Day3/diagrams/day3-db-schema.drawio)
- [Day3 Idempotent Flow](Day3/diagrams/day3-idempotent-flow.drawio)

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
  ![alt text](<images/Screenshot 2026-04-04 133651.png>)
- ✔ Test 2 – Create Post: `POST /posts`
  ![alt text](<images/Screenshot 2026-04-04 134914.png>)
- ✔ Test 3 – Get All: `GET /posts`
  ![alt text](<images/Screenshot 2026-04-04 135044.png>)
- ✔ Test 4 – Get By ID: `GET /posts/1`
  ![alt text](<images/Screenshot 2026-04-04 135728.png>)
  ![alt text](<images/Screenshot 2026-04-04 140001.png>)
- ✔ Test 5 – Update: `PUT /posts/1` (verify bằng GET lại)
  ![alt text](<images/Screenshot 2026-04-04 140242.png>)
  ![alt text](<images/Screenshot 2026-04-04 140347.png>)
- ✔ Test 6 – Delete: `DELETE /posts/1` → `204`, không có body
  ![alt text](<images/Screenshot 2026-04-04 144320.png>)
  ![alt text](<images/Screenshot 2026-04-04 144353.png>)
  ![alt text](<images/Screenshot 2026-04-04 144448.png>)
- ✔ Test 7 – Query Param: `GET /posts?keyword=python`
  ![alt text](<images/Screenshot 2026-04-04 144828.png>)
  ![alt text](<images/Screenshot 2026-04-04 144852.png>)
- ✔ Test 8 – Header: `X-Request-ID: test-123` → log + response header
  ![alt text](<images/Screenshot 2026-04-04 145316.png>)
  ![alt text](<images/Screenshot 2026-04-04 145350.png>)
- ✔ Test 9 – Cookie: `Cookie: user_session=abc123`
  ![alt text](<images/Screenshot 2026-04-04 145932.png>)
  ![alt text](<images/Screenshot 2026-04-04 150010.png>)
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

## 🗺️ Sơ đồ Draw.io Day 4

- [Day4 Architecture](Day4/diagrams/day4-architecture.drawio)
- [Day4 Posts CRUD Flow](Day4/diagrams/day4-posts-crud-flow.drawio)
- [Day4 Test Flow](Day4/diagrams/day4-test-flow.drawio)

---

# 🚀 NGÀY 5 – DATABASE THẬT + ASYNC + MIGRATION

## 🎯 Mục tiêu

- Chuyển storage từ RAM sang PostgreSQL (persistence)
- Dùng Async SQLAlchemy cho non-blocking I/O
- Tách session lifecycle bằng `get_db()`
- Quản lý schema bằng Alembic migration
- Verify dữ liệu còn sau khi restart app

## 🏗️ Cấu trúc chính Day 5

```text
Day5/
├── src/
│   ├── api/posts.py
│   ├── services/post_service.py
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── models/post.py
│   ├── core/config.py
│   └── main.py
├── alembic/
│   ├── env.py
│   └── versions/
├── alembic.ini
├── .env
└── pyproject.toml
```

## ⚙️ Thành phần đã hoàn thành

### 1) Async DB Connection

- `create_async_engine(DATABASE_URL)`
- `async_sessionmaker(...)`
- `async def get_db()` với `async with ... yield ...`

### 2) ORM Model

- `Base(DeclarativeBase)`
- `Post` table với `id`, `title`, `content`
- Mapping bằng `Mapped[]` + `mapped_column()`

### 3) Service Layer dùng DB thật

- CRUD async qua `AsyncSession`
- `create`: `add -> commit -> refresh`
- `read`: `select(Post)` + filter keyword `ILIKE`
- `update/delete`: query theo id, xử lý not found chuẩn

### 4) API Layer orchestration

- Inject DB bằng `Depends(get_db)`
- Endpoint async gọi service bằng `await`
- Giữ chuẩn status code + response model

### 5) Alembic Migration

- `alembic revision --autogenerate`
- `alembic upgrade head`
- Bảng được tạo: `posts`, `alembic_version`

### 6) Docker PostgreSQL

- Container: `postgres-db`
- Port mapping dùng cho app: `localhost:5433`
- `.env` đã cấu hình `DATABASE_URL` theo container

## 🧪 Verify thực tế Day 5

- App load OK với async stack (`asyncpg`, `sqlalchemy`, `alembic`)
- Migration chạy thành công lên `blog_db`
- Insert dữ liệu thành công qua service/API
- Query trong container thấy dữ liệu thật (`SELECT * FROM posts`)

## 🗺️ Sơ đồ Draw.io Day 5

- [Day5 Kiến trúc tổng thể](Day5/diagrams/day5-architecture.drawio)
- [Day5 Luồng CRUD chi tiết](Day5/diagrams/day5-posts-crud-flow.drawio)
- [Day5 Luồng migration chi tiết](Day5/diagrams/day5-migration-flow.drawio)

---

# 📚 KIẾN THỨC ĐÃ HỌC ĐƯỢC (THEO TỪNG NGÀY)

## Ngày 1 – Python nền tảng + Camera

### Kiến thức chính

- Cấu trúc dữ liệu cơ bản: `list`, thao tác duyệt dữ liệu bằng `for`
- Nhập/xuất dữ liệu từ console bằng `input()` và `print()`
- Làm việc với file text: mở file, ghi file, đọc file
- Làm quen OpenCV để mở webcam và hiển thị frame realtime
- Bắt sự kiện phím (`ESC`, `s`) để điều khiển luồng ứng dụng

### Kỹ năng thực hành đạt được

- Xây pipeline mini: nhập dữ liệu → lưu file → đọc lại → thống kê
- Capture ảnh từ webcam và lưu đúng cấu trúc thư mục dataset
- Xử lý vòng lặp realtime cho camera ổn định

### Mindset học được

- Chia bài toán nhỏ trước khi ghép thành luồng lớn
- Kiểm tra từng bước bằng output đơn giản để debug nhanh

## Ngày 2 – AI Attendance System

### Kiến thức chính

- Thiết kế kiến trúc project theo module: `core`, `services`, `gui`, `data`
- Tách rõ logic nghiệp vụ và phần giao diện (separation of concerns)
- Luồng nhận diện cơ bản: camera → detect → recognize → attendance
- Tổ chức dữ liệu dataset theo nhân sự để phục vụ training

### Kỹ năng thực hành đạt được

- Xây GUI có cấu trúc rõ ràng, tách component có thể tái sử dụng
- Cài đặt logic chấm công theo ca làm (`Late`, `Early Leave`)
- Đồng bộ dữ liệu attendance và metadata nhân sự vào SQLite
- Xử lý thao tác xóa nhân sự triệt để + auto retrain model
- Chạy tác vụ nền bằng thread để tránh treo UI

### Mindset học được

- Hệ thống AI thực tế không chỉ có model, mà còn là data + luồng vận hành
- UI mượt cần tách tác vụ nặng sang background

## Ngày 3 – ETL Pipeline + Database

### Kiến thức chính

- Quản lý môi trường và dependency bằng Poetry
- ETL đầy đủ: `Extract -> Transform -> Load`
- Làm việc với SQLAlchemy Core ở mức schema và insert dữ liệu
- Thiết kế schema DB có ràng buộc (`UNIQUE`, index)
- Tư duy idempotent pipeline: chạy nhiều lần không nhân bản dữ liệu

### Kỹ năng thực hành đạt được

- Gọi API có timeout và error handling
- Làm sạch dữ liệu trước khi load vào DB
- Dùng `INSERT OR IGNORE` để chống duplicate
- Dùng context manager (`with engine.begin()`) để auto commit/rollback

### Mindset học được

- Dữ liệu sạch quan trọng hơn dữ liệu nhiều
- Thiết kế schema đúng từ đầu giúp giảm lỗi về sau

## Ngày 4 – FastAPI cơ bản (API Layer)

### Kiến thức chính

- Xây REST API với FastAPI theo chuẩn route HTTP
- Validate request bằng Pydantic schema
- Thiết kế API contract bằng `response_model`
- Triển khai CRUD đầy đủ cho tài nguyên `posts`
- Sử dụng `Path`, `Query`, `Header`, `Cookie` đúng mục đích
- Dùng middleware cho cross-cutting concern (request id logging)

### Kỹ năng thực hành đạt được

- Xử lý status code chuẩn: `201`, `204`, `404`, `422`
- Tách layer `API -> Service -> Storage (RAM)`
- Thêm filter keyword cho endpoint list mà không làm bẩn API layer
- Debug thực tế qua Postman cho từng case endpoint

### Mindset học được

- API layer chỉ nên orchestration, không nhồi business logic
- Contract rõ ràng giúp code dễ maintain và dễ test hơn

## Ngày 5 – Database thật + Async + Migration

### Kiến thức chính

- Chuyển từ in-memory sang PostgreSQL persistence
- Kết nối DB bằng Async SQLAlchemy (`create_async_engine`)
- Quản lý session lifecycle bằng dependency `get_db()` và `yield`
- Define ORM model hiện đại với `DeclarativeBase`, `Mapped[]`, `mapped_column()`
- Dùng Alembic để quản lý migration thay vì `create_all()` thủ công
- Chạy DB qua Docker và hiểu rõ host/container connection

### Kỹ năng thực hành đạt được

- Refactor service sang async CRUD với `AsyncSession`
- Viết query bằng `select(...)`, `scalar_one_or_none()`, `scalars().all()`
- Update/Delete chuẩn với flow query -> mutate -> commit
- Tạo và apply migration: `revision --autogenerate` + `upgrade head`
- Verify end-to-end: API tạo dữ liệu và dữ liệu vẫn tồn tại sau restart

### Mindset học được

- Day 5 là bước chuyển từ code học tập sang tư duy production backend
- Migration là lịch sử tiến hóa schema, không chỉ là “tạo bảng”

## Năng lực tích lũy sau từng ngày

- Từ script đơn giản (Day 1) đến hệ thống có module (Day 2)
- Từ xử lý dữ liệu cục bộ đến pipeline dữ liệu chuẩn (Day 3)
- Từ backend API cơ bản đến contract-first design (Day 4)
- Từ API in-memory đến backend persistent, async, migration-ready (Day 5)

---

# 📌 KẾT LUẬN SAU 5 NGÀY

- ✔ Nắm nền tảng Python, OpenCV, xử lý dữ liệu cơ bản
- ✔ Xây dựng hệ thống AI Attendance có tổ chức
- ✔ Hoàn thành ETL pipeline + database workflow
- ✔ Xây dựng FastAPI API đầy đủ (CRUD, validation, middleware)
- ✔ Hoàn thành nâng cấp Day5: Async DB + PostgreSQL + Alembic migration
- ✔ Tư duy backend theo từng lớp tiến hóa: `API -> DB -> Production-ready`

👉 Sẵn sàng bước sang Day 6 để làm các phần nâng cao: pagination, tối ưu query, auth/security, logging nâng cao.
