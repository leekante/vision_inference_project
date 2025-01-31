# from flask import Flask, render_template, url_for
# import sqlite3
# import os

# app = Flask(__name__)

# DB_PATH = "defective_products.db"
# IMAGE_FOLDER = "static/images_folder2"

# def get_defective_data():
#     """데이터베이스에서 결함 데이터를 가져오는 함수"""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT filename, missing_elements FROM defects")
#     rows = cursor.fetchall()
#     conn.close()
#     return rows

# @app.route("/")
# def index():
#     """웹 페이지 렌더링"""
#     defective_data = get_defective_data()
    
#     # 이미지 파일명만 추출하여 static 경로에 맞게 조정
#     formatted_data = []
#     for filename, missing_elements in defective_data:
#         image_name = os.path.basename(filename)  # 파일명만 가져옴
#         # image_path example : static/images_folder2/ 경로에 있는 이미지 경로를 가져온 것,
#         image_path = url_for('static', filename=f'images_folder2/{image_name}')
#         formatted_data.append((image_path, image_name, missing_elements))
    
#     return render_template("index.html", defective_data=formatted_data)

# if __name__ == "__main__":
#     app.run(debug=True)


# app.py

from flask import Flask, render_template, url_for
import sqlite3
import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Matplotlib 백엔드 설정 (GUI 오류 방지)
# matplotlib.use('Agg')

app = Flask(__name__)

DB_PATH = "defective_products.db"
IMAGE_FOLDER = "./images_folder2"

# 한글 폰트 설정 (Windows 기준)
# 그래프 그릴떄, 글씨가 깨지는 문제가 있어서, 해당 코드를 추가해줘야 했음..
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows 기본 한글 폰트
font_prop = fm.FontProperties(fname=font_path)
plt.rc('font', family=font_prop.get_name())

def get_defective_data():
    """데이터베이스에서 결함 데이터를 가져오는 함수"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT filename, missing_elements FROM defects")
    rows = cursor.fetchall()
    conn.close()
    #print(rows)
    '''
    [('rotated_image.jpg', 'HOLE, BOOTSEL, Raspberry PICO, OSCILLATOR, CHIPSET'), ('test_back_spin.jpg', 'BOOTSEL, Raspberry PICO, CHIPSET')]
    [('rotated_image.jpg', 'HOLE, BOOTSEL, Raspberry PICO, OSCILLATOR, CHIPSET'), ('test_back_spin.jpg', 'BOOTSEL, Raspberry PICO, CHIPSET')]
    '''
    return rows



def generate_defect_chart():
    print("🔄 그래프 생성 중...")
    """부품별 공정률 그래프 생성 (이미지 개수 기준으로)"""
    defective_data = get_defective_data()

    # 이미지 폴더 내 파일 목록 가져오기
    image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    total_image_count = len(image_files)  # 이미지 파일 개수 계산

    # 부품별 놓친 개수 집계
    defect_counts = {
        "HOLE": 0, "BOOTSEL": 0, "Raspberry PICO": 0,
        "OSCILLATOR": 0, "CHIPSET": 0, "USB": 0
    }

    for _, missing_elements in defective_data:
        if missing_elements:
            missing_list = missing_elements.split(", ")
            for part in missing_list:
                if part in defect_counts:
                    defect_counts[part] += 1

    # 공정률 계산
    yield_rates = {}
    for part in defect_counts.keys():
        defective = defect_counts[part]  # 불량품 개수
        yield_rate = ((total_image_count - defective) / total_image_count) * 100  # 공정률 계산
        yield_rates[part] = yield_rate  # 공정률 저장

    # 그래프 크기 조정
    plt.figure(figsize=(12, 7))

    # 막대 그래프 (불량품 개수)
    fig, ax1 = plt.subplots()
    ax1.bar(defect_counts.keys(), defect_counts.values(), color='skyblue', label="불량품 개수")
    ax1.set_xlabel("부품")
    ax1.set_ylabel("불량품 개수", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")

    # 선 그래프 (공정률%)
    ax2 = ax1.twinx()
    ax2.plot(defect_counts.keys(), yield_rates.values(), color='red', marker='o', linestyle='dashed', label="공정률 (%)")
    ax2.set_ylabel("공정률 (%)", color="red")
    ax2.tick_params(axis="y", labelcolor="red")

    # 제목 및 레이아웃
    plt.title("부품별 불량품 및 공정률 분석")
    fig.tight_layout()

    # 그래프 저장
    chart_path = os.path.join("static", "defect_chart.png")
    plt.savefig(chart_path)
    plt.close()

    return chart_path

@app.route("/")
def index():
    """웹 페이지 렌더링"""
    defective_data = get_defective_data()
    
    # 이미지 파일명만 추출하여 static 경로에 맞게 조정
    formatted_data = []
    for filename, missing_elements in defective_data:
        image_name = os.path.basename(filename)
        image_path = url_for('static', filename=f'images_folder2/{image_name}')
        formatted_data.append((image_path, image_name, missing_elements))

    # 그래프 생성
    chart_path = generate_defect_chart()
    
    return render_template("index.html", defective_data=formatted_data, chart_path=chart_path)

if __name__ == "__main__":
    app.run(debug=True)
