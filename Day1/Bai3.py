# đọc file bai2.txt và in ra , đếm số dòng trong file
# kiến thức sử dụng : file handling, exception handling
filename = "bai2.txt"
try:
    with open(filename, "r") as file:
        print("Nội dung file:")
        print(file.read())
except FileNotFoundError:
    print(f"File {filename} không tồn tại.")        