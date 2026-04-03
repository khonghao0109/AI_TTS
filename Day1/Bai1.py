# nhập ds 5 sinh viên và in ra danh sách sinh viên 
# kiến thức sử dụng : list, input, loop[for, while]
#----- có 2 cách tạo danh sách : ds = [] và ds = list()
# .append() để thêm phần tử vào cuối danh sách

ds_sv1 = []
ds_sv2 = list("Khong Hao")
ds_sv3 = list(["Khong Hao","Le Duy"]) #--> đối với list nhiều phần tử  
print(ds_sv2)
print(ds_sv3)

for i in range(5):
    name_sv1 = input(f"Nhap ten sinh vien thu {i+1}: ")
    
    # kiểm tra điều kiện nếu tên trống
    while name_sv1 == "":
        print("ten sinh vien khong duoc de trong")
        name_sv1 = input(f"Nhap lai ten sinh vien thu {i+1}: ")
        
    ds_sv1.append(name_sv1)    

print("Danh sach sinh vien lop sv1")
print(ds_sv1)