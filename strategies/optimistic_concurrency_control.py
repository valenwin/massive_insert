import psycopg2

from utils import main, conn_params


def increment_counter_with_occ():
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()
    try:
        for _ in range(10000):
            while True:
                # Fetch the current counter and version
                cursor.execute("SELECT counter, version FROM user_counter WHERE user_id = 1")
                counter, version = cursor.fetchone()
                new_counter = counter + 1
                new_version = version + 1

                # Attempt to update the counter and version if the version hasn't changed
                cursor.execute("UPDATE user_counter SET counter = %s, version = %s WHERE user_id = %s AND version = %s",
                               (new_counter, new_version, 1, version))
                conn.commit()

                # Check if the row was updated
                if cursor.rowcount > 0:
                    break
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        # Rollback the transaction in case of an error
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main(counter_method=increment_counter_with_occ)
