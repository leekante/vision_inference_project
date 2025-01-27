# import cv2
# import numpy as np

# # 이미지 읽기
# image = cv2.imread('image3.jpg', cv2.IMREAD_COLOR)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # 이미지 영역을 제한해서, 가져오면 인식률이 좋을 듯

# # 이미지 블러 처리 (노이즈 제거)
# gray = cv2.medianBlur(gray, 5)

# # HoughCircles 함수로 원 감지
# circles = cv2.HoughCircles(
#     gray, 
#     cv2.HOUGH_GRADIENT, dp=1.2, minDist=30, 
#     param1=50, param2=30, minRadius=10, maxRadius=100
# )

# # 원이 감지되었다면
# if circles is not None:
#     circles = np.round(circles[0, :]).astype("int")
    
#     # 원 경계 그리기
#     for (x, y, r) in circles:
#         # 원의 중심에 원 그리기
#         cv2.circle(image, (x, y), r, (0, 255, 0), 4)
#         # 원의 중심점에 점 찍기
#         cv2.circle(image, (x, y), 2, (0, 0, 255), 3)

# # 결과 이미지 출력
# cv2.imshow('Detected Circles', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

import cv2
import numpy as np

# 이미지 읽기
image = cv2.imread('image3.jpg', cv2.IMREAD_COLOR)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 관심 영역 (ROI) 설정: 예를 들어, 상단 100px, 좌측 100px 부터 400x400 크기로 설정
roi = gray[100:500, 100:500]

# 이미지 블러 처리 (노이즈 제거)
roi = cv2.medianBlur(roi, 5)

# 캐니 엣지 감지
edges = cv2.Canny(roi, 10, 40)

# 원 감지 (캐니 엣지 결과를 입력으로 사용)
circles = cv2.HoughCircles(
    edges, 
    cv2.HOUGH_GRADIENT, dp=1.2, minDist=30, 
    param1=50, param2=30, minRadius=10, maxRadius=100
)

# 원이 감지되었다면
if circles is not None:
    circles = np.round(circles[0, :]).astype("int")
    
    # 원 경계 그리기
    for (x, y, r) in circles:
        # 원의 중심에 원 그리기
        cv2.circle(image, (x + 100, y + 100), r, (0, 255, 0), 4)  # ROI를 고려한 좌표 보정
        # 원의 중심점에 점 찍기
        cv2.circle(image, (x + 100, y + 100), 2, (0, 0, 255), 3)

# 결과 이미지 출력
cv2.imshow('Detected Circles', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

