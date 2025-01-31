import time
import serial
import numpy as np
import os
import cv2
from rembg import remove
from PIL import Image
import requests
from requests.auth import HTTPBasicAuth
import sqlite3

# 시리얼 포트 설정
ser = serial.Serial("/dev/ttyACM0", 9600)

# 카메라 초기화
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Camera Error")
    exit(-1)

#  -------------------------------------------------------
# DB 설정
DB_PATH = "defective_products.db"

# SQLite 데이터베이스 연결
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 테이블 생성 (없다면 생성)
cursor.execute("""
CREATE TABLE IF NOT EXISTS defects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    missing_elements TEXT
)
""")

#  -------------------------------------------------------

# 저장할 폴더 설정
save_folder = '7.final_project/static/processed_folder'
os.makedirs(save_folder, exist_ok=True)

# Crop 영역 설정
CROP_X, CROP_Y, CROP_W, CROP_H = 100, 100, 1000, 220  

# 정상 피코의 외곽선 길이 범위 설정
MIN_CONTOUR_LENGTH = 2000
MAX_CONTOUR_LENGTH = 4000

# YOLO API 설정
YOLO_API_URL = "https://suite-endpoint-api-apne2.superb-ai.com/endpoints/a3c73094-5e81-4302-9a99-e91068c3bec1/inference"
AUTH = HTTPBasicAuth("kdt2025_1-21", "RM6dU9G9K05me2jsNSLXh3HMAFEoNLMH1C6rsY6W")

# 배경 제거 함수
def remove_background_with_rembg(image):
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # from rembg import remove
    output = remove(pil_image)
    result_image = np.array(output)
    return cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR)

# 회전 각도 및 외곽선 길이 계산
def calculate_rotation_and_contour(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, None, None  

    longest_contour = max(contours, key=cv2.arcLength)  
    rect = cv2.minAreaRect(longest_contour)  
    angle = rect[2]
    
    if rect[1][0] < rect[1][1]:  
        angle += 90
    
    contour_length = cv2.arcLength(longest_contour, True)
    return angle, contour_length, longest_contour

# 이미지 회전 함수
def rotate_image(img, angle):
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(img, rotation_matrix, (w, h))

# 실시간 처리 루프
while True:
    data = ser.read()
    if data == b"0":  
        time.sleep(2)
        ret, img = camera.read()
        if not ret:
            print("Failed to capture image")
            continue

        # 1. 이미지 Crop 및 배경 제거
        cropped_img = img[CROP_Y:CROP_Y + CROP_H, CROP_X:CROP_X + CROP_W]
        img_without_background = remove_background_with_rembg(cropped_img)

        # 2. 회전 각도 및 외곽선 길이 계산
        rotation_angle, contour_length, longest_contour = calculate_rotation_and_contour(img_without_background)
        
        if rotation_angle is not None and contour_length is not None:
            rotated_img = rotate_image(img, rotation_angle)

            if longest_contour is not None:
                cv2.drawContours(rotated_img, [longest_contour], -1, (0, 0, 255), 2)

            # 3. 피코 길이 판단
            if MIN_CONTOUR_LENGTH <= contour_length <= MAX_CONTOUR_LENGTH:
                print(f"Normal Pico detected with contour length: {contour_length}")
            else:
                print(f"Defective Pico detected with contour length: {contour_length}")

            # 4. 이미지 저장
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            img_filename = os.path.join(save_folder, f"pico_{timestamp}.jpg")
            cv2.imwrite(img_filename, rotated_img)
            print(f"Image saved: {img_filename}")

            # 5. YOLO API 요청
            _, img_encoded = cv2.imencode('.jpg', rotated_img)
            response = requests.post(
                YOLO_API_URL,
                auth=AUTH,
                files={"file": ("image.jpg", img_encoded.tobytes(), "image/jpeg")}
            )

            response_data = response.json()
            objects = response_data.get("objects", [])

            # 6. 객체 개수 세기
            object_counts = {"HOLE": 0, "BOOTSEL": 0, "Raspberry PICO": 0, "OSCILLATOR": 0, "CHIPSET": 0, "USB": 0}
            
            for obj in objects:
                if obj['class'] in object_counts:
                    object_counts[obj['class']] += 1

            # 7. 결함 확인
            missing_elements = [k for k, v in object_counts.items() if (k == "HOLE" and v < 3) or v < 1]

            if missing_elements:
                cursor.execute("INSERT INTO defects (filename, missing_elements) VALUES (?, ?)",
                               (img_filename, ", ".join(missing_elements)))
                conn.commit()
                print(f"{img_filename}: Defective - Missing elements: {missing_elements}")
            else:
                print(f"{img_filename}: Normal")

            # 8. 시리얼 신호 전송
            ser.write(b"1")
        else:
            print("No contours detected, skipping frame.")

    if cv2.waitKey(1) & 0xFF == 27:  
        break

camera.release()
cv2.destroyAllWindows()
