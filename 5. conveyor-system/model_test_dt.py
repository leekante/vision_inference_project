#
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

'''
(1, 'C:/Users/kante/Desktop/dosan_robot/ai_1/vision-ai-inference-practice-main/test_img.jpg', 'HOLE, BOOTSEL, Raspberry PICO, OSCILLATOR, CHIPSET, USB')
(2, 'C:/Users/kante/Desktop/dosan_robot/ai_1/vision-ai-inference-practice-main/test_img.jpg', 'BOOTSEL, Raspberry PICO, CHIPSET')
'''