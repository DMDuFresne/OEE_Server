import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


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
                availability DOUBLE PRECISION,
                performance DOUBLE PRECISION,
                quality DOUBLE PRECISION,
                oee DOUBLE PRECISION
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

    # Ensure the data is a dictionary with the necessary keys
    required_keys = {'availability', 'performance', 'quality', 'oee', 'timestamp'}
    if not isinstance(oee_data, dict) or not required_keys.issubset(oee_data.keys()):
        return {
            "error":
                "Data must be a dictionary with keys: 'availability', 'performance', 'quality', 'oee', 'timestamp'"
        }, 400

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
            "INSERT INTO oee_data (availability, performance, quality, oee, time) VALUES (%s, %s, %s, %s, %s)",
            (
                oee_data['availability'],
                oee_data['performance'],
                oee_data['quality'],
                oee_data['oee'],
                oee_data['timestamp']
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

