# 차목, 이름이 겹치면 데이터셋에 안올라갈수도 있는 문제 있음,

import os
import cv2
# 기존 폴더 경로와 저장 폴더 경로 설정
source_folder = "path/to/source/folder"
destination_folder = "path/to/destination/folder"

# 저장 폴더가 없으면 생성
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)
# 크롭할 영역 비율 (이미지 크기 대비 상대적인 값)
crop_ratio = 0.1  # 이미지의 10%를 크롭
# 폴더 내 파일 처리
for filename in os.listdir(source_folder):
    # 이미지 파일만 처리 (예: jpg, png)
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        # 이미지 경로 설정
        img_path = os.path.join(source_folder, filename)
        # 이미지 읽기
        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to read {filename}. Skipping...")
            continue
        # 이미지 크기 가져오기
        h, w, _ = img.shape
        # 크롭할 영역 계산
        x_start = int(w * crop_ratio)
        y_start = int(h * crop_ratio)
        x_end = int(w * (1 - crop_ratio))
        y_end = int(h * (1 - crop_ratio))
        # 크롭 수행
        cropped_img = img[y_start:y_end, x_start:x_end]
        # 저장 경로 설정
        save_path = os.path.join(destination_folder, filename)
        # 크롭한 이미지 저장
        cv2.imwrite(save_path, cropped_img)
        print(f"Saved cropped image: {save_path}")
print("All images have been processed and saved.")