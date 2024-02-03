import psycopg2

from utils import connection_pool, main


def lost_update_counter():
    # Get a connection from the pool
    conn = connection_pool.getconn()
    cursor = conn.cursor()
    try:
        for i in range(10000):
            # Start a new transaction
            # Ensure autocommit is off to manually manage transactions
            conn.autocommit = False
            cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1 FOR UPDATE")
            counter = cursor.fetchone()[0]
            counter += 1
            cursor.execute("UPDATE user_counter SET counter = %s WHERE user_id = %s", (counter, 1))
            # Commit the transaction
            conn.commit()
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        # Rollback the transaction in case of an error
        conn.rollback()
    finally:
        cursor.close()
        # Return the connection to the pool
        connection_pool.putconn(conn)


if __name__ == "__main__":
    main(counter_method=lost_update_counter)
