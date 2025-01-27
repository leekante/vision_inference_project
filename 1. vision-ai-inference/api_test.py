import requests

## get 요청,
response = requests.get("http://192.168.10.48:8081/data")

## 응답 출력
print(f"Get 요청 상태 코드 : {response.status_code}")
print(f"Get 요청 응답 내용 : {response.json()}")

# post 요청
data = {
  "name" : "이강태",
  "group" : "a-1조"
}

response = requests.post("http://192.168.10.48:8081/data", json=data)

# 응답 출력
print(f"post 요청 상태 코드 : {response.status_code}")
print(f"post 요청 응답 내용 : {response.json()}")