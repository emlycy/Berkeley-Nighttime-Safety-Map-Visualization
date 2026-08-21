import sqlite3

data_txt = "1.2.police_call_severe_data.txt"
data_sql = "police_call_raw_data.sqlite"

#read .txt file into a list
call_type = list()
with open(data_txt, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        call_type.append(line)



#Create another SQL table
conn = sqlite3.connect(data_sql)
curs = conn.cursor()

curs.execute('DROP TABLE IF EXISTS Severe_Calls')

curs.execute('''
    CREATE TABLE IF NOT EXISTS Severe_Calls (
        id TEXT PRIMARY KEY,
        time TEXT,
        call_type TEXT,
        address TEXT
    )
''')

for i in range(len(call_type)):
    curs.execute('''
        INSERT OR IGNORE INTO Severe_Calls (id, time, call_type, address)
        SELECT id, time, call_type, address
        FROM Calls
        WHERE call_type = ?
    ''', 
        (call_type[i],)
)
conn.commit()

curs.execute('''
    SELECT call_type, 
        COUNT(*) as count 
    FROM Severe_Calls 
    GROUP BY call_type 
    ORDER BY count DESC
''')

severe_data = curs.fetchall()
conn.commit()

print(severe_data)
conn.close()

print("Success!")
