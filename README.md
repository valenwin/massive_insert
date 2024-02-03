# PostgreSQL Concurrency Control Project

## Overview

This project demonstrates several methods for handling concurrent database operations in PostgreSQL, focusing on
incrementing a counter. It covers in-place updates, row-level locking, and optimistic concurrency control. The goal is
to illustrate how to manage concurrent updates safely and efficiently, ensuring data integrity and performance.

## Requirements

- PostgreSQL
- Python 3
- `psycopg2` Python library
- A PostgreSQL database with the following table structure:

```sql
CREATE TABLE user_counter
(
    user_id SERIAL PRIMARY KEY,
    counter INTEGER NOT NULL,
    version INTEGER NOT NULL
);
```

## Setup

1. **Database Configuration**: Ensure your PostgreSQL database is running and accessible. Create the `user_counter`
   table as described above.

2. **Python Environment**: Set up a Python virtual environment and install the required packages:

```bash
python3 -m venv venv
source venv/bin/activate
pip install psycopg2
```

3. **Database Connection Parameters**: Update the database connection parameters in the scripts to match your PostgreSQL
   setup. These parameters include `dbname`, `user`, `password`, and `host`.

## Running the Scripts

The project includes several scripts demonstrating different concurrency control methods:

1. **In-Place Update**: This script performs in-place updates to the counter, committing each update as a separate
   transaction.

```python
python
in_place_update.py
```

2. **Row-Level Locking**: This script uses `SELECT ... FOR UPDATE` to lock rows during update operations, preventing
   lost updates.

```python
python
row_level_locking.py
```

3. **Optimistic Concurrency Control**: This script uses a versioning system to handle concurrent updates optimistically,
   retrying updates if a version conflict is detected.

```python
python
optimistic_concurrency_control.py
```

## Measuring Execution Time

Each script measures and prints the total execution time for completing the update operations. This allows for
performance comparison between the different concurrency control methods.

## Notes

- The execution time and efficiency can vary based on the number of concurrent clients and the database server's
  configuration.
- Ensure proper error handling and database connection management to maintain data integrity and application stability.

## License

This project is open-sourced under the MIT License.
