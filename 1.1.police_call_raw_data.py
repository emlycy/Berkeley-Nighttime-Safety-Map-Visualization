import csv
import sqlite3

data_csv = "callsforservice.csv" 
data_sql = "police_call_raw_data.sqlite"

conn = sqlite3.connect(data_sql)
curs = conn.cursor()

curs.execute("""
CREATE TABLE IF NOT EXISTS Calls (
    id TEXT PRIMARY KEY,
    time TEXT,
    call_type TEXT,
    address TEXT
)
""")

with open(data_csv, "r", encoding="utf-8") as f_csv:
    csv_reader = csv.reader(f_csv)

    next(csv_reader, None)

    for row in csv_reader:
        if len(row) < 8:
            continue

        id = row[0].strip()
        time = row[1].strip()
        call_type = row[2].strip()  
        address = row[7].strip()  

        curs.execute('''
            INSERT OR IGNORE INTO Calls (id, time, call_type, address)
            VALUES (?,?,?,?);
            ''',
            (id, time, call_type, address),
        )

conn.commit()

curs.execute('''
    SELECT call_type, 
        COUNT(*) as count
    FROM Calls
    GROUP BY call_type
    ORDER BY count DESC
''')

data_call_type = curs.fetchall()

for row in range(len(data_call_type)): 
    print(data_call_type[row])

conn.close()

print("Success!")
