# pico_dataset.py


import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('defective_products.db')
cursor = conn.cursor()

# SELECT 쿼리로 모든 데이터 조회
cursor.execute("SELECT * FROM defects")

# 조회된 데이터를 모두 가져오기
rows = cursor.fetchall()

# 데이터 출력
for row in rows:
    print(row)

# 연결 종료
conn.close()

# '''
# (1, 'C:/Users/kante/Desktop/dosan_robot/ai_1/vision-ai-inference-practice-main/test_img.jpg', 'HOLE, BOOTSEL, Raspberry PICO, OSCILLATOR, CHIPSET, USB')
# (2, 'C:/Users/kante/Desktop/dosan_robot/ai_1/vision-ai-inference-practice-main/test_img.jpg', 'BOOTSEL, Raspberry PICO, CHIPSET')
# '''

# ---------------------------------------------------------------------------------------------------------

# sqlite3 dataset의 데이터들 모두 지우고 싶을 떄,
# import sqlite3

# DB_PATH = "defective_products.db"

# # 데이터베이스 연결
# conn = sqlite3.connect(DB_PATH)
# cursor = conn.cursor()

# # 테이블의 모든 데이터 삭제
# cursor.execute("DELETE FROM defects")

# # 변경 사항 저장 (COMMIT)
# conn.commit()

# # 삭제 후 테이블이 비었는지 확인
# cursor.execute("SELECT * FROM defects")
# rows = cursor.fetchall()
# print("Remaining rows:", rows)  # 빈 리스트([])가 출력되면 삭제 성공

# # 연결 종료
# conn.close()
