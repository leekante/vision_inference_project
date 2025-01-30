# jin.py

import os
import cv2
import numpy as np


# crop영역 설정
CROP_X, CROP_Y, CROP_W, CROP_H = 100, 100, 1000, 220  # 필요에 따라 값 수정

# 경계선 검출 + 회전 함수
def process_and_rotate(img):
    '''
    1.crop img
    2.gray scale / gausian blur
    3.edge canny
    4.contour(윤곽선)
    5.윤곽선 그리기
    
    6. 가장긴변 찾기
    7. 회전 각도 계산
    8. 최종 회전 각도 조정
    9. 원본 이미지에서, 회전각도 만큼 회전
    10. 회전후, 이미지 크기를 원본 크기에 맞추고,
      회전각도만큼 회전하도록 설정
    '''
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
        return cropped_img
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
    # 8. 원본 이미지에서 회전 각도만큼 회전
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    # 회전 후 이미지 크기를 원본 크기에 맞추고, 회전 각도만큼만 회전하도록 설정
    rotated = cv2.warpAffine(img, rotation_matrix, (w, h))
    return rotated

# img_path = "C:/Users/kante/Desktop/dosan_robot/ai_1/vision-ai-inference-practice-main/images_folder/image_20250124_174000.jpg"
# img_path = "C:/Users/kante/Desktop/dosan_robot/ai_1/vision-ai-inference-practice-main/test_img.jpg"
img_path =  "C:/Users/kante/Desktop/dosan_robot/ai_1/vision-ai-inference-practice-main/images_folder/image_20250124_173954.jpg"
# 이미지를 넘길때는 OPENCV로 이미지를 읽어서 보내야 함
img_test = cv2.imread(img_path)

# 이미지 처리
processed_img = process_and_rotate(img_test)
cv2.imshow("Processed Video", processed_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# # 현재 시간으로 파일명 생성
# timestamp = time.strftime("%Y%m%d_%H%M%S")
# img_filename = os.path.join(save_folder, f"image_{timestamp}.jpg")
# # 처리된 이미지 저장
# cv2.imwrite(img_filename, processed_img)