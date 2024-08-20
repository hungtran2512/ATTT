import cv2

# Thông tin NVR và camera
username = "admin"
password = "admin"
nvr_ip = "192.168.1.100"
port = "554"
channel = 1  # Camera số 1
subtype = 0  # Main stream

rtsp_url = f"rtsp://{username}:{password}@{nvr_ip}:{port}/cam/realmonitor?channel={channel}&subtype={subtype}"

output_image_path = r"C:\Users\phatt\Desktop\Server may tinh\captured_image.jpg"

cap = cv2.VideoCapture(rtsp_url)

ret,frame = cap.read()

# Hàm chụp ảnh camera
def capture():
    cv2.imwrite(output_image_path, frame)
    print(f"Capture has been save at {output_image_path}")

if not cap.isOpened():
    print("Không thể kết nối tới camera.")
    exit()

while True:
    if not ret:
        print("Không thể nhận khung hình từ camera.")
        break
    # Cần coi camera thì bỏ # dòng này
    # cv2.imshow(f'Camera {channel}', frame)

    capture()


cap.release()
cv2.destroyAllWindows()