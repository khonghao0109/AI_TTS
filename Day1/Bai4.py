# mở webcam, hiển thị video realtime , nhấn esc để thoát
# kiến thức sử dụng : opencv, video capture, loop, key event
import cv2
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Không thể mở webcam")
    exit()

print("Đang mở webcam... Nhấn 'Esc' để thoát.")
while True:
    ret, frame = cam.read()
    if not ret:
        print("Không thể đọc khung hình từ webcam")
        break
    cv2.imshow("Webcam", frame)
    
    key = cv2.waitKey(1)
    if key == 27:  # 27 là mã ASCII của phím 'Esc'
        print("Đang thoát...")
        break
    
cam.release()
cv2.destroyAllWindows()