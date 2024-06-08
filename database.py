import firebase_admin
from firebase_admin import credentials, db
import json
import time

def initialize_firebase(cred_path, db_url):
    """
    Khởi tạo Firebase Admin SDK.

    Args:
    - cred_path: Đường dẫn đến tệp JSON chứa thông tin xác thực.
    - db_url: URL của Firebase Realtime Database.
    """
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': db_url
    })

def save_data_to_json(data, file_path):
    """
    Lưu dữ liệu vào tệp JSON.

    Args:
    - data: Dữ liệu cần lưu.
    - file_path: Đường dẫn đến tệp JSON.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def fetch_and_save_data(ref_path, file_path):
    """
    Tải dữ liệu từ Firebase và lưu vào tệp JSON.

    Args:
    - ref_path: Đường dẫn đến vị trí dữ liệu trong Firebase Realtime Database.
    - file_path: Đường dẫn đến tệp JSON.
    """
    ref = db.reference(ref_path)
    data = ref.get()
    save_data_to_json(data, file_path)
    print("Dữ liệu đã được tải và lưu lại")

def listener(event):
    """
    Hàm xử lý sự kiện khi dữ liệu thay đổi.

    Args:
    - event: Sự kiện thay đổi dữ liệu.
    """
    print("Dữ liệu thay đổi tại đường dẫn: ", event.path)
    fetch_and_save_data('/', 'firebase_data.json')

def start_listening(ref_path):
    """
    Bắt đầu lắng nghe sự kiện thay đổi dữ liệu từ Firebase.

    Args:
    - ref_path: Đường dẫn đến vị trí dữ liệu trong Firebase Realtime Database.
    """
    ref = db.reference(ref_path)
    ref.listen(listener)

def main():
    cred_path = "key.json"
    db_url = "https://aidigitalsignage-7f781-default-rtdb.firebaseio.com/"  # Thay your-database-name bằng tên database của bạn
    ref_path = "/"  # Lắng nghe toàn bộ dữ liệu trong Firebase Realtime Database

    # Khởi tạo Firebase
    initialize_firebase(cred_path, db_url)

    # Kiểm tra nếu đã có sẵn file firebase_data.json
    try:
        with open('firebase_data.json', 'r', encoding='utf-8') as f:
            print("Đã tìm thấy tệp firebase_data.json, sẽ cập nhật khi có thay đổi.")
    except FileNotFoundError:
        # Nếu không có file, tải và lưu dữ liệu ban đầu
        print("Không tìm thấy tệp firebase_data.json, sẽ tạo mới.")
        fetch_and_save_data(ref_path, 'firebase_data.json')

    # Bắt đầu lắng nghe sự kiện thay đổi dữ liệu
    start_listening(ref_path)

    # Giữ chương trình chạy để lắng nghe sự kiện
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Lắng nghe kết thúc")

if __name__ == "__main__":
    main()
