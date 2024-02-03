import psycopg2

from utils import connection_pool, main


def in_place_update_counter():
    conn = connection_pool.getconn()
    cursor = conn.cursor()
    try:
        for _ in range(10000):
            cursor.execute("UPDATE user_counter SET counter = counter + 1 WHERE user_id = %s", (1,))
            conn.commit()
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        # Rollback the transaction in case of an error
        conn.rollback()
    finally:
        cursor.close()
        connection_pool.putconn(conn)


if __name__ == "__main__":
    main(counter_method=in_place_update_counter)
