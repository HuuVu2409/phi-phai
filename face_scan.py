import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


# Biến toàn cục để lưu trữ bounding box của các khuôn mặt đã phát hiện trước đó
prev_faces = []

# Tải mô hình nhận diện độ tuổi và giới tính
age_net = cv2.dnn.readNetFromCaffe('model/deploy_age2.prototxt', 'model/age_net.caffemodel')
gender_net = cv2.dnn.readNetFromCaffe('model/deploy_gender2.prototxt', 'model/gender_net.caffemodel')

# Các nhãn độ tuổi và giới tính
age_list = ['Newborn(0-2)', 'Kid (4-6)', 'Teenager(8-12)', 'Youngster (15-20)', 'Adult (25-32)', 'Middle-aged (38-43)', 'Elderly (48-53)', 'Old folk  (60-100)']
gender_list = ['Male', 'Female']

def initialize_capture(width=640, height=480):
    """Khởi tạo kết nối video từ webcam và đặt kích thước khung hình."""
    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)
    return cap

def load_face_cascade(harcascade_path):
    """Tải bộ phân loại Haar Cascade từ đường dẫn."""
    return cv2.CascadeClassifier(harcascade_path)

def detect_faces(face_cascade, img_gray):
    """Phát hiện các khuôn mặt trong khung hình thang độ xám."""
    return face_cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

def predict_age_gender(face_img):
    """Dự đoán tuổi và giới tính của khuôn mặt trong ảnh."""
    blob = cv2.dnn.blobFromImage(face_img, 1.0, (227, 227), (104.0, 177.0, 123.0), swapRB=False)
    
    # Dự đoán giới tính
    gender_net.setInput(blob)
    gender_preds = gender_net.forward()
    gender = gender_list[gender_preds[0].argmax()]
    
    # Dự đoán độ tuổi
    age_net.setInput(blob)
    age_preds = age_net.forward()
    age = age_list[age_preds[0].argmax()]
    
    return gender, age

def draw_faces(img, faces):
    """Vẽ hình chữ nhật quanh các khuôn mặt được phát hiện và hiển thị thông tin tuổi, giới tính."""
    for (x, y, w, h) in faces:
        face_img = img[y:y+h, x:x+w].copy()
        
        # Dự đoán tuổi và giới tính
        gender, age = predict_age_gender(face_img)
        
        # Vẽ bounding box và thông tin tuổi, giới tính
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(img, f'{gender}, {age}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
    return img

def stabilize_faces(faces):
    """Cố định bounding box: chỉ cập nhật khi có sự thay đổi lớn."""
    global prev_faces
    
    if len(faces) == 0:
        prev_faces = []
        return []
    
    if len(prev_faces) == 0:
        prev_faces = faces
        return faces
    
    distances = [((x - prev_x) ** 2 + (y - prev_y) ** 2) ** 0.5 for (prev_x, prev_y, _, _) in prev_faces for (x, y, _, _) in faces]
    
    if any(dist > 20 for dist in distances):
        prev_faces = faces
        return faces
    else:
        return prev_faces

def show_image(window_name, img):
    """Hiển thị hình ảnh trong cửa sổ OpenCV."""
    cv2.imshow(window_name, img)

def main():
    harcascade_path = "model/haarcascade_frontalface_default.xml"
    window_name = "Face Detection"
    
    # Khởi tạo webcam và bộ phân loại khuôn mặt
    cap = initialize_capture()
    face_cascade = load_face_cascade(harcascade_path)

    while True:
        # Đọc một khung hình từ video
        success, img = cap.read()
        if not success:
            break

        # Chuyển đổi khung hình sang thang độ xám
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Phát hiện khuôn mặt
        faces = detect_faces(face_cascade, img_gray)

        # Cố định bounding box
        stabilized_faces = stabilize_faces(faces)

        # Vẽ các khuôn mặt được phát hiện
        img_with_faces = draw_faces(img, stabilized_faces)

        # Hiển thị hình ảnh
        show_image(window_name, img_with_faces)

        # Kiểm tra phím 'q' để thoát vòng lặp
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Giải phóng bộ nhớ và đóng tất cả các cửa sổ OpenCV
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
