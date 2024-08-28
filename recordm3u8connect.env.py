import os
import subprocess
import threading
import keyboard
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

# Lấy các đường dẫn RTSP từ biến môi trường
rtsp_urls = [
    os.getenv('RTSP_URL_CAMERA_1'),
    os.getenv('RTSP_URL_CAMERA_2'),
    os.getenv('RTSP_URL_CAMERA_3'),
    os.getenv('RTSP_URL_CAMERA_4'),
    os.getenv('RTSP_URL_CAMERA_5'),
    os.getenv('RTSP_URL_CAMERA_6'),
    os.getenv('RTSP_URL_CAMERA_7'),
    os.getenv('RTSP_URL_CAMERA_8'),
    os.getenv('RTSP_URL_CAMERA_9')
]

base_output_path = os.getenv('OUTPUT_PATH').strip("'")
hls_time = os.getenv('HLS_TIME')
hls_list_size = int(os.getenv('HLS_LIST_SIZE'))

# Biến lưu các tiến trình camera
processes = [None] * len(rtsp_urls)

def clean_old_files(camera_dir):
    """Xóa các tập tin .ts và .m3u8 cũ trong thư mục camera."""
    files = sorted([f for f in os.listdir(camera_dir) if f.endswith('.ts') or f.endswith('.m3u8')],
                    key=lambda x: os.path.getmtime(os.path.join(camera_dir, x)))
    # Giữ lại các tập tin mới nhất dựa trên giá trị HLS_LIST_SIZE
    if len(files) > hls_list_size:
        for file in files[:-hls_list_size]:
            os.remove(os.path.join(camera_dir, file))

def process_camera(index, rtsp_url):
    if rtsp_url:
        group_dir = os.path.join(base_output_path, f'group{(index-1)//3 + 1}')
        camera_dir = os.path.join(group_dir, f'camera{index}')
        os.makedirs(camera_dir, exist_ok=True)
        output_name = os.getenv('OUTPUT_NAMES').split(',')[index-1].strip("'")

        # Xóa các tập tin .ts và .m3u8 cũ trước khi khởi động lại
        clean_old_files(camera_dir)

        command = [
            'ffmpeg',
            '-rtsp_transport', 'tcp',
            '-i', rtsp_url,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-hls_time', hls_time,
            '-hls_list_size', str(hls_list_size),
            '-hls_flags', 'delete_segments+append_list',
            '-hls_segment_filename', os.path.join(camera_dir, f'{output_name}_%03d.ts'),
            '-f', 'hls',
            os.path.join(camera_dir, f'{output_name}.m3u8')
        ]

        print(f'Starting camera {index} with URL {rtsp_url}')
        
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        def stream_log(stream, prefix):
            for line in iter(stream.readline, ''):
                print(f'{prefix}: {line.strip()}')

        stdout_thread = threading.Thread(target=stream_log, args=(process.stdout, f'Camera {index} STDOUT'))
        stderr_thread = threading.Thread(target=stream_log, args=(process.stderr, f'Camera {index} STDERR'))

        stdout_thread.start()
        stderr_thread.start()

        return process
    else:
        print(f'No RTSP URL found for camera {index}')
        return None

def start_all_cameras():
    global processes
    threads = []
    for i in range(len(rtsp_urls)):
        if processes[i] is None:
            print(f'Initializing thread for camera {i + 1}')
            thread = threading.Thread(target=lambda i=i: processes.__setitem__(i, process_camera(i + 1, rtsp_urls[i])))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

def start_camera(index):
    global processes
    if processes[index] is None:
        print(f'Starting camera {index + 1}')
        processes[index] = process_camera(index + 1, rtsp_urls[index])

def stop_camera(index):
    global processes
    if processes[index]:
        print(f'Stopping camera {index + 1}')
        processes[index].terminate()
        processes[index].wait()
        processes[index] = None

def stop_all_cameras():
    global processes
    for i in range(len(rtsp_urls)):
        stop_camera(i)

def handle_keypress(event):
    key = event.name
    if key == 'a':
        stop_all_cameras()
    elif key == '0':
        stop_all_cameras()
        start_all_cameras()
    elif key in map(str, range(1, 10)):
        index = int(key) - 1
        if processes[index] is None:
            start_camera(index)
        else:
            stop_camera(index)
    elif key == 'r':
        stop_all_cameras()
        start_all_cameras()


start_all_cameras()

keyboard.on_press(handle_keypress)

keyboard.wait()
