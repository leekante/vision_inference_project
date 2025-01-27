# 동영상 수집 

# 프레임단위 저장 -> 추론 적용 -> 동영상 만들기 // 한번에

import cv2
import os

video_path = "downloaded_video.mp4"
output_path = "output_video4.mp4"

# videocapture로, 동영상에서 각 프레임 읽어옴.
# cap -> 비디오 파일을 다룰수 있는 여러 속성, 메서드가 존재,,
cap = cv2.VideoCapture(video_path)

# 비디오 속성 추출 (프레임 너비, 높이, FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# 비디오 라이터 객체 생성 (출력 동영상 파일)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # mp4 포맷
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

##
# 모델 생성,
from ultralytics import YOLO
import os
model = YOLO("yolov8n.pt")

# 프레임 단위로 비디오 읽기,

cv2.namedWindow("Image")

while cap.isOpened():
    ret, frame = cap.read() # <- 비디오의 다음 프레임 읽기,
    if not ret: # 비디오를 끝까지 읽으면, ret,이 False가 됨,
      break
      
    # 모델이, 프레임에서 객체를 감지 -> results
    # yolo 라이브러리에서 제공하는 Results 클래스 객체로 구성,
    # result 객체는 리스트로 반환, _ 각 프레임의 감지 결과가 포함
    # results[0]은 results 객체이다.
    
    # 단일객체 - frame 
    results = model(frame)
    
    # 객체를 감지한 결과를 프레임에 그림,
    # results[0]은 감지 결과중, 첫번째 이미지
    
    # Plot 메서드는, results[0]
    # plot메서드로, 바운딩박스, 라벨을 그림,
    result_frame = results[0].plot()
    cv2.imshow("Image", result_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
    # out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    # videowriter out객체,에 저장
    out.write(result_frame)

cap.release()
out.release()
cv2.destroyAllWindows()
