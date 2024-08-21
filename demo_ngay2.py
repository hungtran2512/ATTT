import cv2
import time
import os

# Thông tin NVR và camera
username = "admin"
password = "admin"
nvr_ip = "192.168.1.100"
port = "554" # Port mặc định
channel = 1  # Camera số 1
subtype = 0  # Main stream
path = 0

rtsp_url = f"rtsp://{username}:{password}@{nvr_ip}:{port}/cam/realmonitor?channel={channel}&subtype={subtype}"

output_path = f"D:\\Project\\Server may tinh\\video_{path}.avi"

list_camera = [1,2,3]

def Record_Video(sec):
    video = cv2.VideoCapture(rtsp_url)
    if not video.isOpened():
        print("No found camera!")
        exit

    width = int(video.get(3))
    height = int(video.get(4))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (width,height))
    start_time = time.time()
    while True:
        ret,frame = video.read()
        if not ret:
            break

        cv2.imshow("RTSP", frame)
    
        # Ghi khung hình vào tệp video
        out.write(frame)
    
        # Kiểm tra thời gian đã trôi qua
        elapsed_time = time.time() - start_time
        if elapsed_time > sec:  # Dừng lại sau 10 giây
            break
    
        # Nhấn phím 'q' để thoát sớm hơn 10 giây
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

        video.release
        out.release
        cv2.destroyAllWindows

for i in list_camera:
    path = i
    rtsp_url = f"rtsp://{username}:{password}@{nvr_ip}:{port}/cam/realmonitor?channel={path}&subtype={subtype}"
    output_path = f"D:\\Project\\Server may tinh\\video_{path}.avi"
    Record_Video(10)