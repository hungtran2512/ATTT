import cv2
import os
import subprocess
import requests

# Cấu hình GitHub
repository_url = "https://github.com/Ziiiqaztyu/gittest.git"
local_repo_path = r"E:\nothing"  # Đường dẫn lưu ảnh

def get_next_image_number(path):
    """Lấy số tiếp theo cho tên ảnh."""
    files = os.listdir(path)
    numbers = []
    for file in files:
        if file.endswith(".jpg"):
            try:
                number = int(file.split('.')[0].split('_')[-1])
                numbers.append(number)
            except ValueError:
                pass
    return max(numbers, default=0) + 1

def run_git_command(command):
    """Chạy lệnh Git và xử lý lỗi."""
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during git command '{' '.join(command)}': {e}")

# Bước 1: Chụp ảnh và lưu vào repository local
camera = cv2.VideoCapture(0)
ret, frame = camera.read()

if ret:
    # Lấy số ảnh tiếp theo
    image_number = get_next_image_number(local_repo_path)
    image_name = f"captured_image_{image_number}.jpg"
    image_path = os.path.join(local_repo_path, image_name)

    # Lưu ảnh
    cv2.imwrite(image_path, frame)
    print(f"Ảnh đã được lưu tại {image_path}")

    # Chuyển đến thư mục chứa repository
    os.chdir(local_repo_path)

    # Khởi tạo repository nếu chưa được khởi tạo
    if not os.path.exists(".git"):
        run_git_command(["git", "init"])
        run_git_command(["git", "remote", "add", "origin", repository_url])

    # Đồng bộ hóa với GitHub trước khi đẩy các thay đổi
    try:
        run_git_command(["git", "pull", "origin", "master", "--allow-unrelated-histories"])
    except subprocess.CalledProcessError as e:
        print(f"Error during git pull: {e}")
        # Xử lý lỗi nếu cần, có thể thêm mã để giải quyết xung đột

    # Thực hiện các lệnh Git để đẩy ảnh lên GitHub
    run_git_command(["git", "add", image_name])
    run_git_command(["git", "commit", "-m", f"Add new image: {image_name}"])
    run_git_command(["git", "push", "--set-upstream", "origin", "master"])
    print("Ảnh đã được đẩy lên GitHub.")
else:
    print("Không thể chụp ảnh từ camera.")
camera.release()

# Bước 2: Tải ảnh từ GitHub về máy khi cần
image_url = f"https://raw.githubusercontent.com/Ziiiqaztyu/gittest/master/{image_name}"  # Sử dụng nhánh master
response = requests.get(image_url)

if response.status_code == 200:
    # Lưu ảnh xuống máy
    with open(f"downloaded_{image_name}", "wb") as file:
        file.write(response.content)
    print("Ảnh đã được tải về máy.")
else:
    print(f"Không thể tải ảnh từ GitHub. HTTP Status Code: {response.status_code}")

# Bước 3: Xóa ảnh khi nhấn phím 'd'
print("Nhấn 'd' để xóa ảnh khỏi GitHub.")
key = input()  # Nhận phím từ người dùng

if key == 'd':
    # Xóa ảnh khỏi local repository
    os.remove(image_path)
    print(f"Ảnh {image_name} đã được xóa khỏi local.")

    # Thực hiện lệnh Git để xóa ảnh khỏi GitHub
    run_git_command(["git", "rm", image_name])
    run_git_command(["git", "commit", "-m", f"Remove image: {image_name}"])
    run_git_command(["git", "push"])
    print(f"Ảnh {image_name} đã được xóa khỏi GitHub.")
