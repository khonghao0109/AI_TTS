# Nhập tên + thời gian, sau đó lưu vào file bai2.txt
# kiến thức sử dụng : file handling, string format input,
from datetime import datetime
listname = []
listtime = []
filename = "bai2.txt"

for i in range(3):
    name = input(f"Nhap ten thu {i+1}:")
    now = datetime.now()
    listname.append(name)
    listtime.append(now.strftime("%Y-%m-%d %H:%M:%S"))
    
with open(filename, "a") as file:
    file.write("Danh sach ten va thoi gian:\n")
    for name, time in zip(listname, listtime):
        file.write(f"{name} - {time}\n")