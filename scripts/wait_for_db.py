import time
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                host=os.getenv("POSTGRES_HOST"),
                port=os.getenv("POSTGRES_PORT")
            )
            conn.close()
            print("Database is ready!")
            break
        except psycopg2.OperationalError:
            print("Waiting for database...")
            time.sleep(1)

if __name__ == "__main__":
    wait_for_db() 