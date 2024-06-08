import os
import pygame
from moviepy.editor import VideoFileClip

def get_video_files(directory):
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv')
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.lower().endswith(video_extensions)]

def play_default_ads(video_directory):
    # Lấy danh sách các tệp video
    video_files = get_video_files(video_directory)

    if not video_files:
        print("Không tìm thấy video nào trong thư mục.")
        return

    # Khởi tạo Pygame
    pygame.init()

    # Thiết lập chế độ toàn màn hình
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Digital Signage")

    # Lấy kích thước màn hình
    screen_width, screen_height = screen.get_size()

    # Biến điều khiển vòng lặp chính
    running = True

    # Phát video trong vòng lặp vô hạn
    video_index = 0
    while running:
        video = video_files[video_index]
        # Sử dụng moviepy để phát video
        clip = VideoFileClip(video)

        # Tính toán tỷ lệ để video hiển thị toàn màn hình mà không bị méo
        scale_factor = min(screen_width / clip.w, screen_height / clip.h)
        scaled_width = int(clip.w * scale_factor)
        scaled_height = int(clip.h * scale_factor)
        clip = clip.resize((scaled_width, scaled_height))

        # Phát video với âm thanh và tốc độ bình thường
        clip.preview(fullscreen=True)
        
        # Kiểm tra sự kiện để bỏ qua hoặc thoát
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Chuyển đến video tiếp theo nếu vẫn đang chạy
        if running:
            video_index = (video_index + 1) % len(video_files)

    pygame.quit()

# Ví dụ cách sử dụng hàm
# video_directory = r'C:\download\Ads'
# play_ads(video_directory)


