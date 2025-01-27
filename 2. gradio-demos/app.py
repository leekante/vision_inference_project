import cv2
import gradio as gr
import requests
import numpy as np
from PIL import Image
from requests.auth import HTTPBasicAuth


## 가상의 비전 AI API URL (예: 객체 탐지 API)

# <- vision ai api 엔드포인트 url 에 해당
VISION_API_URL = "" 
# <- 인증에 필요한 팀정보, API키 설정정
TEAM = ""
ACCESS_KEY = ""


def process_image(image):
    # 이미지를 OpenCV 형식으로 변환
    # opencv 에서 처리하기 위해 numpy 배열로 변환한다.
    # 이미지 색상 공간을 RGB => BGR 로 변환한다 / opencv는 BGR로 변환
    
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 이미지를 API에 전송할 수 있는 형식으로 변환
    _, img_encoded = cv2.imencode(".jpg", image)

    # API 호출 및 결과 받기 - 실습1

    # API 결과를 바탕으로 박스 그리기 - 실습2

    # BGR 이미지를 RGB로 변환
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(image)


# Gradio 인터페이스 설정
iface = gr.Interface(
    fn=process_image,
    inputs=gr.Image(type="pil"),
    outputs="image",
    title="Vision AI Object Detection",
    description="Upload an image to detect objects using Vision AI.",
)

# 인터페이스 실행
iface.launch()
