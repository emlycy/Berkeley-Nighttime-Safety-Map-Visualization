import sqlite3

data_sql = "police_call_raw_data.sqlite"
conn = sqlite3.connect(data_sql)
curs = conn.cursor()

#create a table for nighttime(9pm-6am) severe calls
curs.execute('DROP TABLE IF EXISTS Night_Severe_Calls')

curs.execute('''
    CREATE TABLE IF NOT EXISTS Night_Severe_Calls (
        id TEXT PRIMARY KEY,
        time TEXT,
        call_type TEXT,
        address TEXT
    )
''')

curs.execute('''
    INSERT OR IGNORE INTO Night_Severe_Calls (id, time, call_type, address)
    SELECT id, time, call_type, address
    FROM Severe_Calls
    WHERE CAST(substr(time, instr(time, ' ') + 1, 2) AS INTEGER) >= 21
       OR CAST(substr(time, instr(time, ' ') + 1, 2) AS INTEGER) < 6
''')

conn.commit()

curs.execute('''
    SELECT call_type, 
        COUNT(*) as count 
    FROM Night_Severe_Calls 
    GROUP BY call_type 
    ORDER BY count DESC
''')

nighttime_data = curs.fetchall()

for row in nighttime_data:
    print(row)

conn.close()

print("Success!")
