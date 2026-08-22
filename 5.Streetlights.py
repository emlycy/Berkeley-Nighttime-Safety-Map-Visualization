import csv
import sqlite3

data_csv = "streetlights.csv"  # 실제 가로등 CSV 파일명으로 수정해 주세요!
data_sql = "streetlights.sqlite"

conn = sqlite3.connect(data_sql)
curs = conn.cursor()

curs.execute("DROP TABLE IF EXISTS Streetlights")

curs.execute('''
    CREATE TABLE IF NOT EXISTS Streetlights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lat REAL,
        lng REAL,
        address TEXT
    )
''')

with open(data_csv, "r", encoding="utf-8") as f_csv:
    csv_reader = csv.reader(f_csv)
    next(csv_reader)  

    for row in csv_reader:
        if len(row) > 38:
            continue
            
        lat = float(row[8].strip()) 
        lng = float(row[9].strip()) 
        address = row[30].strip() 

        curs.execute('''
            INSERT OR IGNORE INTO Streetlights (lat, lng, address)
            VALUES (?,?,?)
            ''',
            (lat, lng, address)
        )

conn.commit()

conn.close()
print("Success!")