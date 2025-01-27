import cv2
import numpy as np

# 이미지 읽기
image = cv2.imread('image3.jpg')

# ----

# 사각형 감지 -> cv2.findContours()


# ----

# 대비 강화하기 (CLAHE)
# 이미지를 BGR -> LAB 변환
lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
l, a, b = cv2.split(lab)

# CLAHE 생성 및 L 채널에 적용
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
l_clahe = clahe.apply(l)

# CLAHE 적용 후 LAB -> BGR 변환
lab_clahe = cv2.merge((l_clahe, a, b))
image_contrast = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)

# BGR에서 HSV로 변환
hsv = cv2.cvtColor(image_contrast, cv2.COLOR_BGR2HSV)

# 검정색 범위 정의 (H, S, V 값 기준으로 설정)
lower_black = np.array([0, 0, 0])       # 검정색의 하한값
upper_black = np.array([180, 255, 40])  # 검정색의 상한값 (밝기 낮은 영역)

# 검정색 영역 마스크 생성
mask = cv2.inRange(hsv, lower_black, upper_black)

# 마스크를 사용하여 흰색/검정색 이미지 생성
result = np.zeros_like(image_contrast)  # 검정 배경 이미지 생성
result[mask > 0] = [255, 255, 255]      # 검정색 영역만 흰색으로 설정

# 결과 이미지 출력
cv2.imshow('Original Image', image)
cv2.imshow('Contrast Enhanced Image', image_contrast)
cv2.imshow('Black Regions Only', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
