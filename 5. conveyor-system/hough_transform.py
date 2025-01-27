import cv2
import numpy as np

# 이미지 읽기
image = cv2.imread('image3.jpg', cv2.IMREAD_COLOR)

# 그레이스케일 변환
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 캐니 엣지 감지
edges = cv2.Canny(gray, 50, 150)
cv2.imshow("Canny Edge Detection", edges)

# HoughCircles 함수로 원 감지 (캐니 엣지 결과를 입력)
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
        cv2.circle(image, (x, y), r, (0, 255, 0), 4)
        # 원의 중심점에 점 찍기
        cv2.circle(image, (x, y), 2, (0, 0, 255), 3)

# 결과 이미지 출력
cv2.imshow('Detected Circles', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
