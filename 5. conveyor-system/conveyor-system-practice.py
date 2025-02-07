# 라즈베리 파이 실행 
#  Raspberry Pi에서 시리얼 통신과 카메라를 활용해 이미지를 캡처하고,
#  이를 API 서버로 전송하는 형태
import time
import serial
import requests
import numpy
from io import BytesIO
from pprint import pprint

import cv2

ser = serial.Serial("/dev/ttyACM0", 9600)

# API endpoint
api_url = ""


def get_img():
    """Get Image From USB Camera

    Returns:
        numpy.array: Image numpy array
    """

    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Camera Error")
        exit(-1)

    ret, img = cam.read()
    cam.release()

    return img


def crop_img(img, size_dict):
    x = size_dict["x"]
    y = size_dict["y"]
    w = size_dict["width"]
    h = size_dict["height"]
    img = img[y : y + h, x : x + w]
    return img


def inference_reqeust(img: numpy.array, api_rul: str):
    """_summary_

    Args:
        img (numpy.array): Image numpy array
        api_rul (str): API URL. Inference Endpoint
    """
    _, img_encoded = cv2.imencode(".jpg", img)

    # Prepare the image for sending
    img_bytes = BytesIO(img_encoded.tobytes())

    # Send the image to the API
    files = {"file": ("image.jpg", img_bytes, "image/jpeg")}

    print(files)

    try:
        response = requests.post(api_url, files=files)
        if response.status_code == 200:
            pprint(response.json())
            return response.json()
            print("Image sent successfully")
        else:
            print(f"Failed to send image. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")

# while 1:로 무한 루프를 돌며 시리얼 포트에서 데이터를 읽고, 
#  그 값이 b"0"일 경우 카메라에서 이미지를 캡처하여 API로 전송
while 1:
    data = ser.read()
    print(data)
    if data == b"0": # 이 b"0"일 경우 카메라에서 이미지를 캡처하여 API로 전송
        img = get_img()
        # crop_info = None
        # crop info -> size dict
        crop_info = {"x": 200, "y": 100, "width": 300, "height": 300}

        if crop_info is not None:
            img = crop_img(img, crop_info)

        cv2.imshow("", img)
        cv2.waitKey(1)
        result = inference_reqeust(img, api_url)
        ser.write(b"1")
    else:
        pass
