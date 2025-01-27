# # remove_background
# remove_background(input_file, output_file)

# rebmg 는 u2-net기반으로 만들어진 라이브러리이다.
from rembg import remove
from PIL import Image
import io

#input_file = "image3.jpg"  # 배경을 제거할 이미지 경로
#output_file = "image4.png"  # 저장할 이미지 경로 (PNG 형식으로 저장하는 것이 투명 배경을 유지)

input_file = "test_img.jpg"  # 배경을 제거할 이미지 경로
output_file = "test_img_back.png"  # 저장할 이미지 경로 (PNG 형식으로 저장하는 것이 투명 배경을 유지)

def remove_background(input_file, output_file, params=None):
    # 이미지 열기
    with open(input_file, 'rb') as f:
        img_bytes = f.read()  # 이미지를 바이트 형식으로 읽기
    
    # 배경 제거
    if params is None:
        out_bytes = remove(img_bytes)
    else:
        out_bytes = remove(data=img_bytes, **params)
    
    # 바이트 데이터를 이미지로 변환 후 저장
    out_img = Image.open(io.BytesIO(out_bytes))
    out_img.save(output_file)

# 배경 제거 함수 실행
remove_background(input_file, output_file)


# --------------------------
import cv2
import numpy as np

# 배경 제거된 이미지 읽기
image = cv2.imread(output_file, cv2.IMREAD_COLOR)
cv2.imshow('Image', image)
#
# 이미지가 제대로 읽혔는지 확인
if image is None:
    print("이미지 읽기 실패")
    exit()

# 그레이스케일로 변환
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 이미지 이진화 (검정색을 구분하기 위해)
_, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY_INV)

# 객체 윤곽선 찾기
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 윤곽선을 그려서 객체를 시각화
image_with_contours = image.copy()

# 윤곽선의 기울기 계산 및 회전
for contour in contours:
    # 객체가 직사각형일 때만 처리
    rect = cv2.minAreaRect(contour)
    angle = rect[2]
    
    # 직사각형의 세로, 가로 길이
    width, height = rect[1]
    print(f"가로: {width}, 세로: {height}")

    # 직사각형의 윤곽선을 이미지에 그리기
    box = cv2.boxPoints(rect)  # 회전된 직사각형의 4개 점
    box = np.int0(box)  # 정수형 좌표로 변환
    cv2.drawContours(image_with_contours, [box], 0, (0, 255, 0), 2)  # 직사각형 그리기

    # 긴 변이 y축에 평행하도록 각도 조정
    if width <= height:
        # 세로가 긴 경우, 기울기를 수직으로 맞추기 위한 회전
        if angle < -45:
            angle = 90 + angle
        
        # 각도를 0으로 맞춰 세로로 평행하게 만들기
        if angle != 0:
            # 회전
            rows, cols = image.shape[:2]
            rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
            rotated_image = cv2.warpAffine(image, rotation_matrix, (cols, rows))

            # 회전된 이미지를 화면에 표시
            cv2.imshow('Rotated Image', rotated_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            # 회전된 이미지를 저장
            success = cv2.imwrite('test_back_spin_vertical.jpg', rotated_image)
            if not success:
                print("이미지 저장 실패")
            else:
                print("이미지 저장 성공")
    else:
        print('11')
