import subprocess
import ffmpeg

# Lệnh terminal bạn muốn chạy
command = 'ffmpeg -i "rtsp://hung:Zaq%4012345@nongdanonlnine.ddns.net:554/cam/realmonitor?channel=1&subtype=0" -c:v copy -c:a copy -f hls -hls_time 10 -hls_list_size 12 -hls_flags delete_segments "C:\\Users\\phatt\\Desktop\\Server may tinh\\test.m3u8"'

# Chạy lệnh bằng subprocess
try:
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("Output:\n", result.stdout)
except subprocess.CalledProcessError as e:
    print("Error:\n", e.stderr)
