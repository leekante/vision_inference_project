## 배경 제거 + 이미지 회전 + 외곽 길이 계산

import time
import serial
import numpy as np
import os
import cv2
from rembg import remove
from PIL import Image

# 시리얼 포트 설정
ser = serial.Serial("/dev/ttyACM0", 9600)

# 카메라 초기화
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Camera Error")
    exit(-1)

# 저장할 폴더 설정
save_folder = 'processed_images'
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# 외곽선 길이 저장을 위한 텍스트 파일 설정
lengths_file = 'contour_lengths.txt'

# Crop 영역 설정 (x, y는 좌상단 좌표, w는 너비, h는 높이)
CROP_X, CROP_Y, CROP_W, CROP_H = 100, 100, 1000, 220  # 필요에 따라 값 수정

# 정상 피코의 외곽선 길이 범위 설정 (예: 2000 ~ 4000 픽셀)
MIN_CONTOUR_LENGTH = 2000
MAX_CONTOUR_LENGTH = 4000

# 배경 제거 함수 (rembg 사용)
def remove_background_with_rembg(image):
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    output = remove(pil_image)
    result_image = np.array(output)
    return cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR)

# 회전 각도 계산 및 외곽선 검출 함수
def calculate_rotation_and_contour(img):
    # 그레이스케일 및 블러링
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    # 윤곽선 검출
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, None, None  # 윤곽선이 없는 경우
    # 가장 큰 윤곽선 기준으로 계산
    longest_contour = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(longest_contour)  # 최소 경계 사각형
    angle = rect[2]
    if rect[1][0] < rect[1][1]:  # OpenCV의 각도 범위 조정
        angle += 90
    contour_length = cv2.arcLength(longest_contour, True)
    return angle, contour_length, longest_contour

# 이미지 회전 함수
def rotate_image(img, angle):
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(img, rotation_matrix, (w, h))

# 외곽선 길이 저장 함수
def save_contour_length(length):
    with open(lengths_file, 'a') as f:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        f.write(f"{timestamp}, {length}\n")

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
        # 1. 이미지 Crop 및 배경 제거
        cropped_img = img[CROP_Y:CROP_Y + CROP_H, CROP_X:CROP_X + CROP_W]
        img_without_background = remove_background_with_rembg(cropped_img)
        # 2. 회전 각도 및 최외곽선 길이 계산
        rotation_angle, contour_length, longest_contour = calculate_rotation_and_contour(img_without_background)
        if rotation_angle is not None and contour_length is not None:
            # 3. 원본 이미지에서 회전
            rotated_img = rotate_image(img, rotation_angle)
            # 4. 회전된 이미지에 외곽선 다시 그리기
            if longest_contour is not None:
                cv2.drawContours(rotated_img, [longest_contour], -1, (0, 0, 255), 2)  # 빨간색 윤곽선
            # 결과를 Pillow로 출력
            pil_img = Image.fromarray(cv2.cvtColor(rotated_img, cv2.COLOR_BGR2RGB))
            pil_img.show()  # PIL로 이미지 표시
            # 5. 피코 길이 판단 및 결과 처리
            if MIN_CONTOUR_LENGTH <= contour_length <= MAX_CONTOUR_LENGTH:
                print(f"Normal Pico detected with contour length: {contour_length}")
            else:
                print(f"Defective Pico detected with contour length: {contour_length}")
            # 외곽선 길이 저장
            save_contour_length(contour_length)
            # 6. 결과 이미지 저장
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            img_filename = os.path.join(save_folder, f"pico_{timestamp}.jpg")
            cv2.imwrite(img_filename, rotated_img)
            print(f"Image saved: {img_filename}")
            # 시리얼 신호 전송
            ser.write(b"1")
        else:
            print("No contours detected, skipping frame.")
    # ESC 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == 27:  # ESC 키
        break
# 자원 해제
camera.release()
cv2.destroyAllWindows()
# 배경까지 날린건데 외곽선 저장하는부분은 필요없어서 빼셔듀 될거같아여