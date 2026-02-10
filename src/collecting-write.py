import pymysql
import time
import random
import string

# MySQL Connection
DB_CONFIG = {
    "host": "",
    "user": "",
    "password": "",
    "database": "",
    "autocommit": True
}

# Data count
NUM_ROWS = 10000
BATCH_SIZE = 1000

def random_string(length = 10):
    return ''.join(random.choices(string.ascii_letters, k=length))

def generate_data(n):
    return [(random_string(10), ) for _ in range(n)]

def insert_single(cursor, data):
    for row in data:
        cursor.execute("INSERT INTO tests(name) VALUES (%s)", row)

def insert_batch(cursor, data, batch_size):
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        cursor.executemany("INSERT INTO tests(name) VALUES (%s)", batch)

def main():
    conn = pymysql.connect(**DB_CONFIG)
    cur = conn.cursor()

    print("Creating table...")
    cur.execute("CREATE TABLE IF NOT EXISTS tests(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")

    print("Truncating table...")
    cur.execute("TRUNCATE TABLE tests")

    print("Inserting single row...")
    data = generate_data(NUM_ROWS)
    start = time.time()
    insert_single(cur, data)
    elapsed_single = time.time() - start
    print(f"Single insert time: {elapsed_single:.2f} seconds")

    cur.execute("TRUNCATE TABLE tests")

    print("Inserting batch...")
    data = generate_data(NUM_ROWS)
    start = time.time()
    insert_batch(cur, data, BATCH_SIZE)
    elapsed_batch = time.time() - start
    print(f"Batch insert time (batch size {BATCH_SIZE}): {elapsed_batch:.2f} seconds")

    print("Deleting table...")
    cur.execute("DROP TABLE IF EXISTS tests")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
