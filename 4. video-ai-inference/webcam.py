# 동영상 수집 

# 프레임단위 저장 -> 추론 적용 -> 동영상 만들기 // 한번에

import cv2
import os

output_path = "output_realtime1.mp4"

# videocapture로, 동영상에서 각 프레임 읽어옴.
# cap = cv2.VideoCapture(video_path)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
  print("web cam 안열림.")
  exit()

# 비디오 속성 추출 (프레임 너비, 높이, FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # mp4 포맷
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# 비디오 라이터 객체 생성 (출력 동영상 파일)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # mp4 포맷

##
# 모델 생성,
from ultralytics import YOLO
import os
model = YOLO("yolov8n.pt")

# 프레임 단위로 비디오 읽기,
while cap.isOpened():
    ret, frame = cap.read() # <- 비디오의 다음 프레임 읽기,
    if not ret: # 비디오를 끝까지 읽으면, ret,이 False가 됨,
      break
      
    # 모델이, 프레임에서 객체를 감지 -> results
    results = model(frame)
    
    result_frame = results[0].plot()    
    
    cv2.imshow("web cam detection", result_frame)
    
    out.write(result_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("종료합니다.")
        break

cap.release()
cv2.destroyAllWindows()

print(f"webcam 객체 인식 결과 : 저장 경로 {output_path}")