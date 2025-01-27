import cv2
import numpy as np

# 이미지 읽기
image = cv2.imread('rotated_image.jpg')

# 이미지가 제대로 읽혔는지 확인
if image is None:
    print("이미지 읽기 실패")
    exit()

# 이미지를 그레이스케일로 변환
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 에지 검출
edges = cv2.Canny(gray, 10, 150, apertureSize=3)

# 허프 변환을 사용하여 이미지에서 직선 찾기
lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

# 기울기 각도 계산
if lines is not None:
    # 첫 번째 직선의 각도를 기준으로 회전 각도를 구함
    for line in lines:
        rho, theta = line[0]
        angle = np.degrees(theta) - 90  # 수평선과의 각도를 기준으로 계산
        
        # 이미지 회전 (기울어진 각도를 반영)
        rows, cols = image.shape[:2]
        rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)

        # 회전된 이미지 크기 계산
        abs_cos = abs(rotation_matrix[0, 0])
        abs_sin = abs(rotation_matrix[0, 1])

        # 회전된 이미지의 크기 계산 (가로, 세로)
        new_cols = int(rows * abs_sin + cols * abs_cos)
        new_rows = int(rows * abs_cos + cols * abs_sin)

        # 회전된 이미지 생성
        rotated_image = cv2.warpAffine(image, rotation_matrix, (new_cols, new_rows))

        # 회전된 이미지를 저장
        success = cv2.imwrite('rotated_image_vertical2.jpg', rotated_image)
        if not success:
            print("이미지 저장 실패")
        else:
            print("이미지 저장 성공")

        # 회전된 이미지를 화면에 표시
        cv2.imshow('Rotated Image', rotated_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
else:
    print('직선 감지 안됨.')

