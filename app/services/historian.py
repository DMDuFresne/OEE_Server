import os
import psycopg2
from flask import jsonify
from dotenv import load_dotenv

load_dotenv()
# TODO Move this functionality into the oee model


def create_oee_data_table():
    try:
        # Establish a connection to the database
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

        # Open a cursor and execute SQL command to create the table
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS oee_data (
                time TIMESTAMPTZ NOT NULL,
                run_time DOUBLE PRECISION,
                total_time DOUBLE PRECISION,
                total_count DOUBLE PRECISION,
                target_count DOUBLE PRECISION,
                good_count DOUBLE PRECISION,
                availability DOUBLE PRECISION,
                performance DOUBLE PRECISION,
                quality DOUBLE PRECISION,
                oee DOUBLE PRECISION,
                object_type INTEGER,
                object_id INTEGER
            )
            """
        )

        try:
            # Add time series hypertable to the table
            cur.execute("SELECT create_hypertable('oee_data', 'time', chunk_time_interval => INTERVAL '1 day')")
        except psycopg2.DatabaseError as hypertable_error:
            # Handle hypertable creation error (table is already a hypertable)
            # You can choose to ignore the error or handle it in a specific way
            print(f"Hypertable creation error: {str(hypertable_error)}")

        # Commit changes and close the connection
        conn.commit()
        cur.close()
        conn.close()

        return {"message": "Successfully created the oee_data table in TimescaleDB"}, 200

    except psycopg2.DatabaseError as e:
        # Handle database errors
        raise e

    except Exception as e:
        # Handle any other errors
        raise e


def insert_oee_data(oee_data):

    required_fields = [
        'run_time',
        'total_time',
        'total_count',
        'target_count',
        'good_count',
        'availability',
        'performance',
        'quality',
        'oee',
        'timestamp',
        'object_type',
        'object_id'
    ]

    for field in required_fields:
        if field not in oee_data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    try:

        # Establish a connection to the database
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

        # Open a cursor and execute SQL commands
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO oee_data (
            run_time, total_time, total_count, target_count, good_count,
            availability, performance, quality, oee, time, object_type, object_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                oee_data['run_time'],
                oee_data['total_time'],
                oee_data['total_count'],
                oee_data['target_count'],
                oee_data['good_count'],
                oee_data['availability'],
                oee_data['performance'],
                oee_data['quality'],
                oee_data['oee'],
                oee_data['timestamp'],
                oee_data['object_type'],
                oee_data['object_id']
            )
        )

        # Commit changes and close the connection
        conn.commit()
        cur.close()
        conn.close()

        return {"message": "OEE data inserted successfully"}, 200

    except psycopg2.DatabaseError as e:

        # Handle database errors
        raise e

    except Exception as e:

        # Handle any other errors
        raise e


# Call the create_oee_data_table function to create the table
create_oee_data_table()
