# YOLO ENDPOINT
# 25/1/28 (4:00 - 5:30)
# https://suite-endpoint-api-apne2.superb-ai.com/endpoints/718f0c2f-1833-4655-9a32-93ca4c833924/inference

# 이미지데이터셋 -> 모델에 넣고,
#  칩셋 요소 인식하는 데이터 보고
#  1. 일정 요소 정하기
#  2. 불량품 기준 일정 성립시, 데이터셋에 넣기
# ---------------------------------
#  3. 데이터셋 시각화


# <이미지지>

# import sqlite3
# import requests
# import cv2
# from requests.auth import HTTPBasicAuth

# IMAGE_FILE_PATH = "C:/Users/kante/Desktop/dosan_robot/ai_1/vision-ai-inference-practice-main/images_folder/image_20250124_174159.jpg"

# DB_PATH = "defective_products.db"  # SQLite database file

# # Setup SQLite database connection
# conn = sqlite3.connect(DB_PATH)
# cursor = conn.cursor()

# # Create table if it doesn't exist
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS defects (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     filename TEXT,
#     missing_elements TEXT
# )
# """)

# # Read the image
# image = cv2.imread(IMAGE_FILE_PATH)

# # Send image to the YOLO endpoint
# image_data = open(IMAGE_FILE_PATH, "rb").read()
# response = requests.post(
#     #url="https://suite-endpoint-api-apne2.superb-ai.com/endpoints/718f0c2f-1833-4655-9a32-93ca4c833924/inference",
#     # DETA_ endpoint 발급
#     url="https://suite-endpoint-api-apne2.superb-ai.com/endpoints/a3c73094-5e81-4302-9a99-e91068c3bec1/inference",
#     auth=HTTPBasicAuth("kdt2025_1-21", "RM6dU9G9K05me2jsNSLXh3HMAFEoNLMH1C6rsY6W"),
#     headers={"Content-Type": "image/jpeg"},
#     data=image_data,
# )

# # Parse the response
# response_data = response.json()
# objects = response_data.get("objects", [])

# # Count the number of occurrences of each object type
# object_counts = {"HOLE": 0, "BOOTSEL": 0, "Raspberry PICO": 0, "OSCILLATOR": 0, "CHIPSET": 0, "USB": 0}

# # Draw bounding boxes and count the detected objects
# for obj in objects:
#     box = obj['box']
#     cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
#     label = f"{obj['class']} ({obj['score']:.2f})"
#     cv2.putText(image, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#     # Increment the object count
#     if obj['class'] in object_counts:
#         object_counts[obj['class']] += 1

# # Check if the object counts meet the criteria for a "normal" product
# missing_elements = []

# # If any required object is missing, note it down
# if object_counts["HOLE"] < 3:
#     missing_elements.append("HOLE")
# if object_counts["BOOTSEL"] < 1:
#     missing_elements.append("BOOTSEL")
# if object_counts["Raspberry PICO"] < 1:
#     missing_elements.append("Raspberry PICO")
# if object_counts["OSCILLATOR"] < 1:
#     missing_elements.append("OSCILLATOR")
# if object_counts["CHIPSET"] < 1:
#     missing_elements.append("CHIPSET")
# if object_counts["USB"] < 1:
#     missing_elements.append("USB")

# # If any elements are missing, store it in the database
# if missing_elements:
#     missing_elements_str = ", ".join(missing_elements)
#     cursor.execute("""
#     INSERT INTO defects (filename, missing_elements) VALUES (?, ?)
#     """, (IMAGE_FILE_PATH, missing_elements_str))
#     conn.commit()
#     print(f"Defective: Missing elements: {missing_elements_str}")
# else:
#     print("Normal")

# # Display the image
# cv2.imshow("Image with detected objects", image)

# # Wait for a key press and close the image window
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# # Close the database connection
# conn.close()



# pico_detection.py
# <2. 이미지 폴더에 대해>
import os
import sqlite3
import requests
import cv2
from requests.auth import HTTPBasicAuth

# 이미지 폴더 경로 설정
# IMAGE_FOLDER_PATH = "C:/Users/kante/Desktop/dosan_robot/ai_1/vision-ai-inference-practice-main/images_folder2/"
IMAGE_FOLDER_PATH = "C:/Users/kante/Desktop/dosan_robot/ai_1/vision-ai-inference-practice-main/images_folder"

DB_PATH = "defective_products.db"  # SQLite database file

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

# DETA (Swin-L)-final_pico_dataset // ENDPOINT
#YOLO_API_URL = "https://suite-endpoint-api-apne2.superb-ai.com/endpoints/a3c73094-5e81-4302-9a99-e91068c3bec1/inference"
YOLO_API_URL = "https://suite-endpoint-api-apne2.superb-ai.com/endpoints/a3c73094-5e81-4302-9a99-e91068c3bec1/inference"
AUTH = HTTPBasicAuth("kdt2025_1-21", "RM6dU9G9K05me2jsNSLXh3HMAFEoNLMH1C6rsY6W")
HEADERS = {"Content-Type": "image/jpeg"}

# 폴더 내 이미지 처리
for filename in os.listdir(IMAGE_FOLDER_PATH):  # <-- 폴더 내 파일 목록 가져오기
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # 이미지 파일만 처리
        image_path = os.path.join(IMAGE_FOLDER_PATH, filename)  # 전체 경로 생성
        
        # 이미지 읽기
        image = cv2.imread(image_path)
        image_data = open(image_path, "rb").read()
        
        # YOLO API 요청
        response = requests.post(YOLO_API_URL, auth=AUTH, headers=HEADERS, data=image_data)
        response_data = response.json()
        objects = response_data.get("objects", [])
        
        # 객체 개수 초기화
        object_counts = {"HOLE": 0, "BOOTSEL": 0, "Raspberry PICO": 0, "OSCILLATOR": 0, "CHIPSET": 0, "USB": 0}
        
        # 객체 감지 및 카운트
        for obj in objects:
            box = obj['box']
            cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
            label = f"{obj['class']} ({obj['score']:.2f})"
            cv2.putText(image, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            if obj['class'] in object_counts:
                object_counts[obj['class']] += 1
        
        # 결함 요소 확인
        missing_elements = []
        if object_counts["HOLE"] < 3:
            missing_elements.append("HOLE")
        if object_counts["BOOTSEL"] < 1:
            missing_elements.append("BOOTSEL")
        if object_counts["Raspberry PICO"] < 1:
            missing_elements.append("Raspberry PICO")
        if object_counts["OSCILLATOR"] < 1:
            missing_elements.append("OSCILLATOR")
        if object_counts["CHIPSET"] < 1:
            missing_elements.append("CHIPSET")
        if object_counts["USB"] < 1:
            missing_elements.append("USB")
        
        # 결함이 있는 경우 데이터베이스에 저장
        if missing_elements:
            missing_elements_str = ", ".join(missing_elements)
            cursor.execute("""
            INSERT INTO defects (filename, missing_elements) VALUES (?, ?)
            """, (filename, missing_elements_str))
            conn.commit()
            print(f"{filename}: Defective - Missing elements: {missing_elements_str}")
        else:
            print(f"{filename}: Normal")
        
        # 이미지 출력
        cv2.imshow("Detected Objects", image)
        cv2.waitKey(500)  # 0이면 키 입력 대기, 500이면 0.5초 대기 후 다음 이미지

cv2.destroyAllWindows()
conn.close()  # 데이터베이스 연결 종료
