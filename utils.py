import threading
import time

import psycopg2
from psycopg2 import pool


def create_table(conn_params):
    """
    Creates a table in the PostgreSQL database.

    Parameters:
    - conn_params: A dictionary with the connection parameters.
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_counter (
        user_id SERIAL PRIMARY KEY,
        counter INTEGER DEFAULT 0,
        version INTEGER DEFAULT 0
    );
    """

    conn = None
    cursor = None
    try:
        # Assuming db_connect is your custom function to establish a database connection
        # Make sure this function is correctly implemented to unpack **conn_params
        conn = psycopg2.connect(**conn_params)  # This should match your db_connect function's expected arguments
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
        print("Table created successfully.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


conn_params = {
    'dbname': 'postgres',
    'user': '',
    'password': '',
    'host': 'localhost'
}
# Initialize the connection pool
connection_pool = pool.SimpleConnectionPool(1, 10, **conn_params)


def db_connect():
    return connection_pool.getconn()


def db_release_conn(conn):
    connection_pool.putconn(conn)


def main(counter_method):
    start_time = time.time()

    threads = []
    for _ in range(10):
        # Create 10 threads
        thread = threading.Thread(target=counter_method)
        threads.append(thread)
        thread.start()

    for thread in threads:
        # Wait for all threads to complete
        thread.join()

    end_time = time.time()
    print(f"Total execution time {counter_method.__name__}: {end_time - start_time} seconds")


if __name__ == "__main__":
    create_table(conn_params)
