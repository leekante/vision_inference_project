# import sys
# import numpy as np
# import cv2

# src = cv2.imread('./image3.jpg', cv2.IMREAD_GRAYSCALE)
# # 이미지를 읽어온다.

# if src is None:
#     print('Image open failed!')
#     sys.exit()
# # 이미지가 없으면 실행하고 종료

# src = cv2.resize(src, dsize=(900, 959))
# # 이미지의 사이즈를 조절한다.

# blr = cv2.GaussianBlur(src, (0, 0), 1.0)
# # 이미지의 잡음을 제거한다.

# # 트렉바를 정의한다.
# def on_trackbar(pos):
#     rmin = cv2.getTrackbarPos('minRadius', 'img')
#     rmax = cv2.getTrackbarPos('maxRadius', 'img')
#     th = cv2.getTrackbarPos('threshold', 'img')
    
#     if th <= 0:
#         th = 1
    
#     # 실질적인 허프변환이 시작되는 부분
#     circles = cv2.HoughCircles(blr, cv2.HOUGH_GRADIENT, 1, 50, param1=120, param2=th, minRadius=rmin, maxRadius=rmax)
#     # 반지름과 threshold를 조절하면서 확인해볼 분이다.

#     dst = src.copy()
#     # 이미지를 복사해서 dst에 저장한다.
    
#     # 원을 검출할 때 실행된다.
#     if circles is not None:
#         circles = np.round(circles[0, :]).astype('int')
#         for circle in circles:
#         # 검출된 원의 개수만큼 돌아서 원을 그린다.
            
#             cx, cy, radius = circle
            
#             cv2.circle(dst, (cx, cy), radius, (255, 0, 0), 2, cv2.LINE_AA)
#             cv2.putText(dst, str(radius), org=(cx, cy), 
#                         fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, 
#                         color=(0,0,255),thickness=3, lineType=cv2.LINE_AA)
#     cv2.imshow('img', dst)

# # 트랙바 생성
# cv2.imshow('img', src)
# cv2.createTrackbar('minRadius', 'img', 0, 100, on_trackbar)
# cv2.createTrackbar('maxRadius', 'img', 0, 150, on_trackbar)
# cv2.createTrackbar('threshold', 'img', 0, 100, on_trackbar)
# cv2.setTrackbarPos('minRadius', 'img', 10)
# cv2.setTrackbarPos('maxRadius', 'img', 80)
# cv2.setTrackbarPos('threshold', 'img', 40)
# cv2.waitKey()
# cv2.destroyAllWindows()


import sys
import numpy as np
import cv2

src = cv2.imread('./image3.jpg', cv2.IMREAD_GRAYSCALE)
# 이미지를 읽어온다.

if src is None:
    print('Image open failed!')
    sys.exit()
# 이미지가 없으면 실행하고 종료

src = cv2.resize(src, dsize=(900, 959))
# 이미지의 사이즈를 조절한다.

blr = cv2.GaussianBlur(src, (0, 0), 1.0)
# 이미지의 잡음을 제거한다.

# 트랙바를 정의한다.
def on_trackbar(pos):
    rmin = cv2.getTrackbarPos('minRadius', 'img')
    rmax = cv2.getTrackbarPos('maxRadius', 'img')
    th = cv2.getTrackbarPos('threshold', 'img')
    
    if th <= 0:
        th = 1
    
    # 실질적인 허프변환이 시작되는 부분
    circles = cv2.HoughCircles(blr, cv2.HOUGH_GRADIENT, 1, 50, param1=120, param2=th, minRadius=rmin, maxRadius=rmax)
    # 반지름과 threshold를 조절하면서 확인해볼 분이다.

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
        if num_circles > 3:  # 검출된 원이 3개 이상일 때
            print(f'1차 검수 합격, 원의 개수: {num_circles}')
    else:
        print('검출된 원이 없습니다.')

    cv2.imshow('img', dst)

# 트랙바 생성
cv2.imshow('img', src)
cv2.createTrackbar('minRadius', 'img', 0, 100, on_trackbar)
cv2.createTrackbar('maxRadius', 'img', 0, 150, on_trackbar)
cv2.createTrackbar('threshold', 'img', 0, 100, on_trackbar)
cv2.setTrackbarPos('minRadius', 'img', 10)
cv2.setTrackbarPos('maxRadius', 'img', 80)
cv2.setTrackbarPos('threshold', 'img', 40)
cv2.waitKey()
cv2.destroyAllWindows()
