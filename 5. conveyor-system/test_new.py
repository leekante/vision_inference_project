import time
import serial
import numpy as np
import os
import cv2
from PIL import Image
import requests
from requests.auth import HTTPBasicAuth
import sqlite3
import uuid
from datetime import datetime
import keyboard
# 시리얼 포트 설정
ser = serial.Serial("/dev/ttyACM0", 9600)
# 데이터베이스 연결
conn = sqlite3.connect('example.db')
cursor = conn.cursor()
# 데이터 삽입 함수
def insert_data(datetime_value, uuid_value, is_defective, defect_reason=None):
    insert_query = '''
    INSERT INTO 제품 (datetime, uuid, is_defective, defect_reason)
    VALUES (?, ?, ?, ?)
    '''
    cursor.execute(insert_query, (datetime_value, uuid_value, is_defective, defect_reason))
    conn.commit()
# superbModel 함수
def superbModel(path):
    # 이미지 경로를 받아서 분석 요청
    image_path = path
    image = Image.open(image_path)
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    _, img_encoded = cv2.imencode(".jpg", image)
    ACCESS_KEY = 'RM6dU9G9K05me2jsNSLXh3HMAFEoNLMH1C6rsY6W'
    response = requests.post(
        url="https://suite-endpoint-api-apne2.superb-ai.com/endpoints/a3c73094-5e81-4302-9a99-e91068c3bec1/inference",
        auth=HTTPBasicAuth("kdt2025_1-21", ACCESS_KEY),
        headers={"Content-Type": "image/jpeg"},
        data=img_encoded.tobytes(),
    )
    return response.json()
# 카메라 초기화
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Camera Error")
    exit(-1)
# 저장할 폴더 설정
save_folder = 'processed_images'
if not os.path.exists(save_folder):
    os.makedirs(save_folder)
# Crop 영역 설정 (x, y는 좌상단 좌표, w는 너비, h는 높이)
CROP_X, CROP_Y, CROP_W, CROP_H = 100, 100, 450, 220  # 필요에 따라 값 수정
# 경계선 검출 및 회전 함수
def process_and_rotate(img):
    # 1. 이미지 Crop
    cropped_img = img[CROP_Y:CROP_Y + CROP_H, CROP_X:CROP_X + CROP_W]
    # 2. 그레이스케일 변환 및 블러링
    gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # 3. 에지 검출 (Canny)
    edges = cv2.Canny(blurred, 50, 150)
    # 4. 윤곽선 검출
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 윤곽선 그리기 (검출된 윤곽선 표시)
    img_with_contours = cropped_img.copy()
    cv2.drawContours(img_with_contours, contours, -1, (0, 0, 255), 2)  # 윤곽선 색상은 빨간색 (0,0,255)
    if not contours:
        # 윤곽선이 없는 경우 Crop한 이미지 반환
        return cropped_img, img_with_contours
    # 5. 가장 긴 변 찾기
    max_length = 0
    longest_contour = None
    for contour in contours:
        rect = cv2.minAreaRect(contour)
        (width, height) = rect[1]
        length = max(width, height)
        if length > max_length:
            max_length = length
            longest_contour = rect
    # 6. 회전 각도 계산
    angle = longest_contour[2]
    # 7. 최종 회전 각도 조정 (긴 변이 항상 수평)
    if longest_contour[1][0] < longest_contour[1][1]:  # 세로가 더 길다면
        angle += 90
    else:
        angle = 0
    # 8. 원본 이미지에서 회전 각도만큼 회전
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    # 회전 후 이미지 크기를 원본 크기에 맞추고, 회전 각도만큼만 회전하도록 설정
    rotated = cv2.warpAffine(img, rotation_matrix, (w, h))
    return rotated, img_with_contours
# 실시간 처리 루프
while True:
    # 시리얼 데이터 읽기
    data = ser.read()
    if data == b"0":  # 신호가 0일 때
        time.sleep(2)
        ret, img = camera.read()
        if not ret:
            print("Failed to capture image")
            continue
        # 이미지 처리 (경계선 검출 및 회전)
        rotated_img, img_with_contours = process_and_rotate(img)
        # 회전된 이미지와 윤곽선 이미지 화면에 출력
        rotated_pil_img = Image.fromarray(cv2.cvtColor(rotated_img, cv2.COLOR_BGR2RGB))  # BGR -> RGB 변환
        contours_pil_img = Image.fromarray(cv2.cvtColor(img_with_contours, cv2.COLOR_BGR2RGB))  # BGR -> RGB 변환
        rotated_pil_img.show(title="Rotated Image")
        contours_pil_img.show(title="Contours Image")
        # 현재 시간으로 파일명 생성
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        img_filename = os.path.join(save_folder, f"image_{timestamp}.jpg")
        # 처리된 이미지 저장
        cv2.imwrite(img_filename, rotated_img)
        # superbModel API 호출
        print("???????")
        dic = superbModel(img_filename)
        pico_dic = {'Raspberry PICO':0, 'BOOTSEL':0, 'OSCILLATOR':0, 'CHIPSET':0, 'HOLE':0, 'USB':0}
        for i in dic['objects']:
            pico_dic[i['class']] += 1
        print(pico_dic)
        print(pico_dic.values())
        if list(pico_dic.values()) < [1, 1, 1, 1, 4, 1]:
            is_defective = 0
        else:
            is_defective = 1
        datetime_value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 현재 날짜와 시간
        uuid_value = str(uuid.uuid4())  # UUID 생성
        defect_reason = None
        insert_data(datetime_value, uuid_value, is_defective, defect_reason)
        print(f"Image saved: {img_filename}")
        # 시리얼 신호 전송
        ser.write(b"1")
# 자원 해제
camera.release()
cv2.destroyAllWindows()
conn.close()