# open cv 라이브러리

import cv2
import os

#img_path = "/Users/igangtae/Desktop/인하대/vision-ai-inference-practice-main/image2.png"
img_path = "C:/Users/kante/Desktop/dosan_robot/ai_1/vision-ai-inference-practice-main/image3.jpg"
print(os.path.exists(img_path))  # True면 경로가 유효, False면 경로 문제 -> True, 이 문제는 아닌거 같음,


img = cv2.imread(img_path)

# 박스칠, 좌표 설정
# pico point
start_point = (366, 470)
end_point = (675, 1071)

# 박스칠, 좌표 설정2
# usb
start_point2 = (513, 999)
end_point2 = (606, 1079)

#
color1 = (0, 255, 0)
color2 = (255, 0, 0)

#
thickness = 2

# 박스 그리기
cv2.rectangle(img, start_point, end_point, color1, thickness)
# cv2.rectangle(img, start_point2, end_point2, color2, thickness)

# opencv 윈도우에 이미지 띄우기,
cv2.imshow("show window", img)

# opencv로 박스 그리고, 이미지 저장하기
#cv2.imwrite("cv2_box_image3.jpg", img)

cv2.waitKey(0)
cv2.destroyAllWindows()

