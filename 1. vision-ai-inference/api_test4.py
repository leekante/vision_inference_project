# 2, 3 연결

# 이미지 좌표 가져오기 _ 2
# 이미지 그리기_3


# opencv에서 처리할수 있는 형태_넘파이 배열
#  로 변환해야 한다

# 2.
import requests
import os
import cv2
import numpy as np
from requests.auth import HTTPBasicAuth

# IMAGE_FOLDER_PATH = "/Users/igangtae/Desktop/인하대/vision-ai-inference-practice-main/images_folder"
IMAGE_FOLDER_PATH = "C:\Users\kante\Desktop\dosan_robot\지능_1\vision-ai-inference-practice-main\images_folder"
image_files_path = [IMAGE_FOLDER_PATH + '/' + f for f in os.listdir(IMAGE_FOLDER_PATH)]

print(image_files_path)
# image = open(IMAGE_LIST[1], "rb").read()


color1 = (0, 255, 0)
thickness = 2

for path in image_files_path[:3]:
  with open(path, "rb") as img_file:
    image_binary = img_file.read()


  response = requests.post(
      url="https://suite-endpoint-api-apne2.superb-ai.com/endpoints/ae6ca04a-3d23-4ba1-8f72-6a5a3183a96a/inference",
      auth=HTTPBasicAuth("kdt2025_1-21", "RM6dU9G9K05me2jsNSLXh3HMAFEoNLMH1C6rsY6W"),
      headers={"Content-Type": "image/jpeg"},
      data=image_binary,
  )

  json_ = response.json()
  
  # OpenCV용 이미지 디코딩
  np_array = np.frombuffer(image_binary, np.uint8)
  image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)  # Numpy 배열을 OpenCV 이미지로 디코딩
  
  # 가져온 (x1, y1) / (x2, y2) 에 cv2로 그리기.
  # print(response['objects'][0]['box'])
  
  for obj in json_['object']:
    class_name = obj['class']
    x1, y1 = obj['box'][0], obj['box'][1]
    x2, y2 =  obj['box'][2], obj['box'][3]
    start_point = (x1, y1)
    end_point = (x2, y2)
    # open cv _ 3 연결
    #   박스 그리기
    cv2.rectangle(image, start_point, end_point, color1, thickness)
    cv2.imshow("show window", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
