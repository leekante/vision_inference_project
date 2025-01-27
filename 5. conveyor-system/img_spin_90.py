import cv2

# 이미지 읽기
image = cv2.imread('image4_spin.png')

#print(image.shape)
# (700, 700, 3)
# 이미지 크기 구하기
height, width = image.shape[:2]

# 가로가 더 긴 경우 회전
if width > height:
    # 90도 회전 (시계방향)
    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

# 결과 이미지 저장 또는 화면에 표시
cv2.imwrite('rotated_image2.jpg', image)  # 회전된 이미지를 저장
# cv2.imshow('Rotated Image', image)  # 화면에 회전된 이미지 표시 (GUI가 동작하면 사용할 수 있음)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
