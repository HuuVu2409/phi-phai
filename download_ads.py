from pytube import YouTube
import os
import time

def download_videos(file_path, download_path):
    video_files = []

    # Mở tệp văn bản chứa các liên kết video
    with open(file_path, 'r') as file:
        # Đọc từng dòng trong tệp và tải video
        for line in file:
            try:
                # Tạo đối tượng YouTube từ liên kết
                yt = YouTube(line.strip())
                # Chọn stream progressive có độ phân giải 720p
                video_stream = yt.streams.filter(res="720p", progressive=True).first()
                if video_stream:
                    # Tải stream
                    video_filename = video_stream.download(output_path=download_path)
                    video_files.append(video_filename)
                    print(f"Downloaded: {yt.title}")
                else:
                    print(f"No suitable 720p progressive stream found for: {yt.title}")
            except Exception as e:
                print(f"Error downloading {line.strip()}: {e}")

    return video_files

def run_with_timer(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f} seconds")
    return result

# Đường dẫn tệp văn bản chứa các liên kết video và thư mục lưu trữ các tệp tải xuống
# file_path = 'C:\\study_document\\datn\\source\\Ads list.txt'
# download_path = 'C:\\study_document\\datn\\source\\Ads'

# Tải video
# video_files = run_with_timer(download_videos, file_path, download_path)

