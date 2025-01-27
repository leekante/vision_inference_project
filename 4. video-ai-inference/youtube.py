import yt_dlp

import cv2
import os

from moviepy.editor import ImageSequenceClip


# ----다운로드 ----------------------------------------
# 다운로드 할, youtube url
url = "https://www.youtube.com/shorts/JRMEpi-4U2Y"

# yt-dlp 설정
ydl_opts = {
  "format": "best",
  "outtmpl": "downloaded_video.%(ext)s",
}

# 다운로드
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
  ydl.download([url])
  

# ----------------------------------------------------


video_path = "downloaded_video.mp4"
cap = cv2.VideoCapture(video_path)

output_dir = "frames"
os.makedirs(output_dir, exist_ok=True)

frame_count = 0
while cap.isOpened():
  ret, frame = cap.read()
  # ret, 잘 읽어들였는지 알수 있는 정보임,
  if not ret:
    break
  frame_path = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
  cv2.imwrite(frame_path, frame)
  frame_count += 1
  
cap.release()
print(f"총 {frame_count}개의 프레임이 저장되었습니다.")

'''
[youtube] JRMEpi-4U2Y: Downloading ios player API JSON
[youtube] JRMEpi-4U2Y: Downloading m3u8 information
[info] JRMEpi-4U2Y: Downloading 1 format(s): 18
[download] downloaded_video.mp4 has already been downloaded
[download] 100% of    1.27MiB
총 531개의 프레임이 저장되었습니다.
'''

# ----------------------------------------------------
# yolov8 pre trained 모델 추론
from ultralytics import YOLO

import os

model = YOLO("yolov8n.pt")

# "frames" 디렉토리 안에 있는 파일과 폴더 목록을 가져옴
frames = os.listdir("frames/")

# 원하는 디렉토리 경로 설정
directory_path = "results"

# 디렉토리가 없으면 생성
if not os.path.exists(directory_path):
    os.makedirs(directory_path)
    print(f"디렉토리 '{directory_path}'가 생성되었어.")
else:
    print(f"디렉토리 '{directory_path}'가 이미 존재해.")

for frame in frames:
  # device ~, 부분은 맥이여서 적은거. 아니면 지우기
  results = model("frames/" + frame)
  
  for result in results:
    result.save(filename="results/" + frame) # <-  pdf 오타, 
    
# ----------------------------------------------------
## 추론된, 프레임으로 다시 만든다.

# 이미지 파일들이 저장된 디렉토리 경로
image_folder = "results"  # 이미지 파일들이 있는 폴더 경로
# fps = int(fps)  # 초당 프레임 수 설정
fps = 30

# 이미지 파일 리스트 가져오기 (예: jpg, png 형식)
image_files = [
    os.path.join(image_folder, img)
    for img in sorted(os.listdir(image_folder))
    if img.endswith((".jpg", ".png"))
]

# 이미지 시퀀스를 이용해 클립 생성
# ImageSequenceCliP 안되면 -> opencv로 묶는법이 있음, 
clip = ImageSequenceClip(image_files, fps=fps)

# 동영상 파일로 저장
output_path = "output_video.mp4"
clip.write_videofile(output_path, codec="libx264")

print(f"동영상이 생성되었습니다: {output_path}")