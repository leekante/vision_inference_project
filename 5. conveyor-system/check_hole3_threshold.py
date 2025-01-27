# min r = 0,
# max r = 12,
# threshold = 19, 로 가정하면 다음과 같다.

import sys
import numpy as np
import cv2

def process_image(image_path, min_radius=0, max_radius=12, threshold=19):
    src = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # 이미지를 읽어온다.
    if src is None:
        print('Image open failed!')
        return
    # 이미지가 없으면 실행하고 종료

    src = cv2.resize(src, dsize=(900, 959))
    # 이미지의 사이즈를 조절한다.

    blr = cv2.GaussianBlur(src, (0, 0), 1.0)
    # 이미지의 잡음을 제거한다.

    # 허프 변환으로 원을 검출
    circles = cv2.HoughCircles(blr, cv2.HOUGH_GRADIENT, 1, 50, param1=120, param2=threshold, minRadius=min_radius, maxRadius=max_radius)

    dst = src.copy()
    # 이미지를 복사해서 dst에 저장한다.

    # 원을 검출할 때 실행된다.
    if circles is not None:
        circles = np.round(circles[0, :]).astype('int')
        for circle in circles:
            # 검출된 원의 개수만큼 돌아서 원을 그린다.
            cx, cy, radius = circle
            cv2.circle(dst, (cx, cy), radius, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(dst, str(radius), org=(cx, cy), 
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, 
                        color=(0,0,255),thickness=3, lineType=cv2.LINE_AA)

        # 원의 개수 출력
        num_circles = len(circles)
        cv2.putText(dst, f"Number of circles: {num_circles}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # 특정 조건에 따라 검수 메시지 출력
        if num_circles > 0:  # 검출된 원이 하나 이상일 때
            print(f'1차 검수 합격, 원의 개수: {num_circles}')
    else:
        print('검출된 원이 없습니다.')

    cv2.imshow('Processed Image', dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 여러 이미지에 대해 처리
image_paths = ['image.png', 'image2.png', 'image3.jpg']  # 이미지 경로 리스트

for image_path in image_paths:
    process_image(image_path, min_radius=0, max_radius=12, threshold=19)
