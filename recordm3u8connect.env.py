from dotenv import load_dotenv
import os
import subprocess
import concurrent.futures

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
hls_list_size = os.getenv('HLS_LIST_SIZE')

def process_camera(index, rtsp_url):
    if rtsp_url:

        group_dir = os.path.join(base_output_path, f'group{(index-1)//3 + 1}')
        camera_dir = os.path.join(group_dir, f'camera{index}')
        
        os.makedirs(camera_dir, exist_ok=True)
        
        output_name = os.getenv('OUTPUT_NAMES').split(',')[index-1].strip("'")
        
        command = [
            'ffmpeg',
            '-rtsp_transport', 'tcp',
            '-i', rtsp_url,
            '-c:v', 'copy',
            '-c:a', 'aac',  
            '-b:a', '128k',
            '-hls_time', hls_time,
            '-hls_list_size', hls_list_size,
            '-hls_flags', 'delete_segments',
            '-hls_segment_filename', os.path.join(camera_dir, f'{output_name}_%03d.ts'),
            '-f', 'hls',
            os.path.join(camera_dir, f'{output_name}.m3u8')
        ]
        
        print(f'Processing camera {index} with URL {rtsp_url}')
        subprocess.run(command)
    else:
        print(f'No RTSP URL found for camera {index}')


with concurrent.futures.ThreadPoolExecutor(max_workers=9) as executor:
    futures = [executor.submit(process_camera, index, url) for index, url in enumerate(rtsp_urls, start=1)]
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()  
        except Exception as e:
            print(f'An error occurred: {e}')
