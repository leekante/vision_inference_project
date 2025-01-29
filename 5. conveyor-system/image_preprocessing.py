
# 경계 인식하고, 배경을 제거

# 해당 데이터로, 모델 재학습시키고 모델 성능 보겠음,

# 1. 배경을 날리는 모델1을 사용하여 데이터셋을 새로 생성한다.
# 2. 해당 데이터셋으로, 라벨링을 진행한다 (대략 300장)
# 3. 컨베이어벨트에서, 칩셋을 캡쳐 <이건 현재 환경에서 할수 없음음> -> 배경 날리는 모델1 진행 -> 2. 해당 이미지로 YOLO모델을 통해 인식

# 4. 인식데이터를 받아서 인식률 확인 + 그래프로 시각화 구현



# -------------------------------------------------------------------------
 
from rembg import remove
from PIL import Image
import io
import os
import cv2
import numpy as np

# 입력 및 출력 폴더 경로
input_folder = "./images_folder"  # 수정된 경로
output_folder = "./images_folder_preprocessing"  # 수정된 경로

# 전처리 이미지 저장 디렉토리가 없으면 생성
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"디렉토리 '{output_folder}'가 생성되었습니다.")
else:
    print(f"디렉토리 '{output_folder}'가 이미 존재합니다.")

# 배경 제거 및 객체 뒤 배경을 흰색으로 변경하는 함수
def remove_background(input_file, output_file, params=None):
    try:
        # 이미지 열기
        with open(input_file, 'rb') as f:
            img_bytes = f.read()
        
        # 배경 제거
        if params is None:
            out_bytes = remove(img_bytes)
        else:
            out_bytes = remove(data=img_bytes, **params)
        
        # 바이트 데이터를 PIL 이미지로 변환
        out_img = Image.open(io.BytesIO(out_bytes))

        # 이미지 모드 확인 및 변환
        if out_img.mode != "RGBA" and out_img.mode != "RGB":
            raise ValueError(f"Unexpected image mode: {out_img.mode}")
        
        # 투명 배경(RGBA)을 흰색 배경(RGB)으로 변환
        if out_img.mode == "RGBA":
            background = Image.new("RGB", out_img.size, (255, 255, 255))
            out_img = Image.alpha_composite(background, out_img)

        # PIL 이미지를 OpenCV 이미지로 변환
        open_cv_image = cv2.cvtColor(np.array(out_img), cv2.COLOR_RGB2BGR)

        # 그레이스케일 변환
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        # 이진화 처리
        _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

        # 객체 윤곽선 찾기
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 윤곽선 그리기
        result_img = open_cv_image.copy()
        cv2.drawContours(result_img, contours, -1, (0, 255, 0), 2)

        # 결과 이미지 저장
        cv2.imwrite(output_file, result_img)
        print(f"이미지 처리 완료: {output_file}")
        
    except Exception as e:
        print(f"이미지 처리 중 오류 발생: {input_file} - {e}")

# 폴더 내 모든 이미지 파일 처리

i = 0 
for file_name in os.listdir(input_folder):
    file_path = os.path.join(input_folder, file_name)
    
    # 파일이 이미지인지 확인
    if file_name.lower().endswith(('png', 'jpg')):
        print(f"처리 중: {file_name}")
        remove_background(file_name, f"pp_img_{i}")
        
    else:
        print(f'이미지 파일이 아니므로 스킵 : {file_name}')



# i = 0
# for image_name in os.listdir(input_folder):
#     input_path = os.path.join(input_folder, image_name)  # 정확한 경로 설정
#     output_img = f"preprocessed_img_{i}.jpg"
#     output_path = os.path.join(output_folder, output_img)  # 출력 경로 설정
    
#     # 이미지 파일만 처리
#     if image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
#         print(f"처리 중: {input_path}")
#         remove_background(input_path, output_path)  # 배경 제거 함수 실행
#         i += 1  # 이미지마다 고유한 이름으로 저장
    
#     else:
#         print(f"이미지 파일이 아니므로 스킵됨: {image_name}")
