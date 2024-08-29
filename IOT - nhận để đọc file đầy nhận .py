import os

# Đường dẫn đến file log
log_file_path = 'D:\\FILE_TOOL\\vscode\\LORA\\output\\log.txt'

def read_log_file(file_path):
    if not os.path.isfile(file_path):
        print(f"File {file_path} không tồn tại!")
        return

    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print("Nội dung của file log:")
            print(content)
    except Exception as e:
        print(f"Có lỗi xảy ra khi đọc file: {e}")

if __name__ == "__main__":
    read_log_file(log_file_path)
