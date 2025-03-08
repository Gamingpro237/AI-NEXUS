import psycopg2

# Replace these with your actual credentials
HOST = "18.237.155.139"
PORT = 5432
DATABASE = "geekleai"
USER = "yash"
PASSWORD = "123456a@"

try:
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        dbname=DATABASE,
        user=USER,
        password=PASSWORD
    )
    print("Connection successful!")
    conn.close()
except Exception as e:
    print("Error connecting to PostgreSQL:", e)
