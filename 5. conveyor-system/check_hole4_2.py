import cv2
import numpy as np
import matplotlib.pyplot as plt

# 이미지 읽기
image = cv2.imread('image.png')

# 이미지가 제대로 읽혔는지 확인
if image is None:
    print("이미지 읽기 실패")
    exit()

# 이미지를 그레이스케일로 변환
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 에지 검출
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# 허프 변환을 사용하여 이미지에서 직선 찾기
lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
print(lines)
# 기울기 각도 계산
if lines is not None:
    for line in lines:
        rho, theta = line[0]
        # 직선의 각도를 계산
        angle = np.degrees(theta) - 90  # 수평선과의 각도를 기준으로 계산
        print(f"Detected line angle: {angle} degrees")

        # 이미지를 회전 (기울어진 각도를 반영)
        rows, cols = image.shape[:2]
        rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
        rotated_image = cv2.warpAffine(image, rotation_matrix, (cols, rows))

        # 회전된 이미지를 화면에 표시
        plt.imshow(cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB))
        plt.title('Rotated Image')
        plt.axis('off')
        plt.show()

        # 회전된 이미지를 저장
        success = cv2.imwrite('rotated_image.jpg', rotated_image)
        if not success:
            print("이미지 저장 실패")
        else:
            print("이미지 저장 성공")
else:
    print("직선 감지 안됨. 이미지는 직각으로 되어있거나 기울기가 미미합니다.")
