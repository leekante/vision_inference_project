import os
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# 원본 이미지 폴더 경로와 증강된 이미지 저장 폴더 경로 설정
input_folder = './images_folder'  # 원본 이미지 폴더 경로

output_folder = 'images_transformed_folder'  # 증강 이미지 저장 폴더 경로
os.makedirs(output_folder, exist_ok=True)  # 출력 폴더 생성

# 데이터 증강기 설정
datagen = ImageDataGenerator(
    rotation_range=30,          # 최대 30도 회전
    width_shift_range=0.2,      # 수평 이동
    height_shift_range=0.2,     # 수직 이동
    shear_range=0.2,            # 전단 변환
    zoom_range=0.2,             # 확대/축소
    horizontal_flip=True,       # 좌우 반전
    fill_mode='nearest'         # 빈 공간은 가장 가까운 픽셀로 채움
)

# 폴더 내 이미지 파일 처리
for file_name in os.listdir(input_folder):
    file_path = os.path.join(input_folder, file_name)

    # 파일이 이미지인지 확인
    if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        # 이미지 로드 및 형식 변환
        img = cv2.imread(file_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # OpenCV 이미지를 RGB로 변환
        img = np.expand_dims(img, axis=0)  # 배치 차원 추가 (1, H, W, C)

        # 증강 이미지 생성 및 저장
        save_prefix = os.path.splitext(file_name)[0]  # 파일 이름에서 확장자 제거
        i = 0
        for batch in datagen.flow(img, batch_size=1, save_to_dir=output_folder,
                                  save_prefix=save_prefix, save_format='jpg'):
            i += 1
            if i >= 5:  # 이미지 당 5개의 증강된 샘플 생성
                break

print("데이터 증강 완료! 증강된 이미지는", output_folder, "폴더에 저장되었습니다.")
