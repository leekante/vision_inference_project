import os
from rembg import remove
from PIL import Image
import io
import cv2
import numpy as np

def process_image(input_file, output_file, output_file_white):
    # Step 1: 배경 제거
    with open(input_file, 'rb') as f:
        img_bytes = f.read()  # 이미지를 바이트 형식으로 읽기

    # 배경 제거 (rembg 사용)
    out_bytes = remove(img_bytes)

    # 바이트 데이터를 이미지로 변환 후, 투명 배경으로 저장
    out_img = Image.open(io.BytesIO(out_bytes))
    out_img.save(output_file)

    # Step 2: 배경을 흰색으로 변경
    img_with_white_bg = out_img.convert("RGBA")
    datas = img_with_white_bg.getdata()

    new_data = []
    for item in datas:
        # 투명한 (알파값 0) 픽셀을 흰색으로 변경
        if item[3] == 0:
            new_data.append((255, 255, 255, 255))  # 흰색 배경
        else:
            new_data.append(item)
    img_with_white_bg.putdata(new_data)
    img_with_white_bg.save(output_file_white)

def process_images_in_folder(images_folder, output_folder):
    # Step 3: 이미지 폴더 내 모든 이미지 처리
    if not os.path.exists(output_folder):  # 출력 폴더가 없으면 생성
        os.makedirs(output_folder)

    # 이미지 폴더에서 모든 파일 이름 가져오기
    image_files = [f for f in os.listdir(images_folder) if os.path.isfile(os.path.join(images_folder, f))]

    for image_file in image_files:
        input_file = os.path.join(images_folder, image_file)
        output_file = os.path.join(output_folder, f"{os.path.splitext(image_file)[0]}_back.png")
        output_file_white = os.path.join(output_folder, f"{os.path.splitext(image_file)[0]}_back_white.png")
        
        print(f"Processing {image_file}...")
        process_image(input_file, output_file, output_file_white)  # 이미지 처리 함수 호출
        print(f"Saved processed images for {image_file}.")

# 사용 예시
images_folder = "C:/Users/kante/Desktop/dosan_robot/ai_1/vision-ai-inference-practice-main/images_folder"  # 원본 이미지들이 있는 폴더
output_folder = "C:/Users/kante/Desktop/dosan_robot/ai_1/vision-ai-inference-practice-main/images_folder_preprocessing"  # 변형된 이미지를 저장할 폴더
process_images_in_folder(images_folder, output_folder)


# 해당 코드로 이미지를 돌려보니, 
# 정상적으로 도는 것도 있고 깨지는 것도 있기 떄문에
#  사실상 해당 방법으로 전처리를 하는 건 적합하지 않다..