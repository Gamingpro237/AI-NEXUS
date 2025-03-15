# database.py
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import pool

# Load the .env file
load_dotenv()

# Read environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "geekleai")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_PORT = os.getenv("DB_PORT", "5432")

# Create a connection pool
try:
    conn_pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    if conn_pool:
        print("Psycopg2 connection pool created successfully!")
except Exception as e:
    print("Error creating connection pool:", e)
    raise

def get_connection():
    """
    Acquire a connection from the pool.
    """
    try:
        conn = conn_pool.getconn()
        return conn
    except Exception as e:
        print("Error getting connection from pool:", e)
        raise

def release_connection(conn):
    """
    Release the connection back to the pool.
    """
    try:
        conn_pool.putconn(conn)
    except Exception as e:
        print("Error releasing connection:", e)
        raise

def close_all_connections():
    """
    Close all connections in the pool (useful for application shutdown).
    """
    try:
        conn_pool.closeall()
        print("All connections in the pool have been closed.")
    except Exception as e:
        print("Error closing all connections:", e)
        raise
