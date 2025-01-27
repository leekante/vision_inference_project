import requests
from requests.auth import HTTPBasicAuth

IMAGE_FILE_PATH = "C:/Users/kante/Desktop/dosan_robot/ai_1/vision-ai-inference-practice-main/rotated_image_vertical.jpg"

image = open(IMAGE_FILE_PATH, "rb").read()

response = requests.post(
    url="https://suite-endpoint-api-apne2.superb-ai.com/endpoints/a3c73094-5e81-4302-9a99-e91068c3bec1/inference",
    auth=HTTPBasicAuth("kdt2025_1-21", "RM6dU9G9K05me2jsNSLXh3HMAFEoNLMH1C6rsY6W"),
    headers={"Content-Type": "image/jpeg"},
    data=image,
)
print(response.json())

# {'objects': [{'class': 'CHIPSET', 'score': 0.6636437177658081,
# 'box': [482, 711, 565, 799]}, {'class': 'HOLE', 'score': 0.41871213912963867,
# 'box': [421, 492, 451, 529]}, {'class': 'HOLE', 'score': 0.4079369008541107,
# 'box': [544, 480, 575, 516]}, {'class': 'USB', 'score': 0.2258417159318924,
# 'box': [561, 881, 608, 943]}]}
  

# yolov6 -n // end point
# https://suite-endpoint-api-apne2.superb-ai.com/endpoints/a3c73094-5e81-4302-9a99-e91068c3bec1/inference