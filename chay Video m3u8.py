import cv2

# Đường dẫn đến file .m3u8
video_path = r'C:\\Users\\phatt\\Desktop\\Server may tinh\\test.m3u8'

# Tạo đối tượng VideoCapture để đọc video từ file
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Không thể mở video.")
else:
    while cap.isOpened():
        ret, frame = cap.read()  # Đọc từng frame của video
        if not ret:
            print("Không thể đọc frame. Hoặc hết video.")
            break

        cv2.imshow('Video', frame)  # Hiển thị frame trên cửa sổ

        # Nhấn 'q' để thoát
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

# Giải phóng đối tượng capture và đóng tất cả cửa sổ
cap.release()
cv2.destroyAllWindows()
