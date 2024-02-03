import psycopg2

from utils import main, conn_params


def row_level_locking_counter():
    # Create a new database connection for each thread
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()
    try:
        for _ in range(10000):
            # Acquire row-level lock
            cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1 FOR UPDATE")
            counter = cursor.fetchone()[0]
            counter += 1
            # Update the counter
            cursor.execute("UPDATE user_counter SET counter = %s WHERE user_id = %s", (counter, 1))
            conn.commit()  # Commit each transaction to release the lock
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        # Rollback the transaction in case of an error
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main(counter_method=row_level_locking_counter)
