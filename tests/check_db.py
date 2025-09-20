import psycopg2

conn = psycopg2.connect(
    dbname="defaultdb",
    user="avnadmin",
    password="DB_Password",
    host="sihteam-6-nmdtalha2411-153.d.aivencloud.com",
    port="15674",
    sslmode="require"
)

cur = conn.cursor()
"""

# 1. Check if any data exists at all
cur.execute('SELECT COUNT(*) FROM public."ingressdata2025";')
print("Total rows:", cur.fetchone()[0])

# 2. See all distinct districts (helps catch spelling/case issues)
cur.execute('SELECT DISTINCT "DISTRICT" FROM public."ingressdata2025";')
print("Districts found:")
for row in cur.fetchall():
    print(row[0])
"""
cur.execute('SELECT * FROM public."ingressdata2025" WHERE "DISTRICT" ILIKE %s;', ("bengaluru south",))
rows = cur.fetchall()
print(rows)

cur.close()
conn.close()
