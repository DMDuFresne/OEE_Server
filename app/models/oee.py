import os
import logging
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv
from contextlib import contextmanager
from datetime import datetime, timezone

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OeeModel:
    connection_pool = None

    def __init__(self, **kwargs):

        # Define the required arguments for OeeModel initialization
        required_arguments = ['good_count', 'total_count', 'run_time', 'total_time', 'target_count']

        # Check for missing required arguments
        missing_arguments = set(required_arguments) - set(kwargs)
        if missing_arguments:
            raise ValueError("Missing required keyword arguments: {}".format(", ".join(missing_arguments)))

        try:

            # Convert and assign the provided values to instance variables
            self.good_count = float(kwargs['good_count'])
            self.total_count = float(kwargs['total_count'])
            self.run_time = float(kwargs['run_time'])
            self.total_time = float(kwargs['total_time'])
            self.target_count = float(kwargs['target_count'])

        except KeyError as ke:
            raise ValueError("Missing required keyword argument: '{}'".format(ke))

        except TypeError as te:
            raise ValueError("Error initializing OeeModel: " + str(te))

    def calculate_quality(self):

        # Check if good_count and total_count are numbers
        if not isinstance(self.good_count, (int, float)) or not isinstance(self.total_count, (int, float)):
            raise ValueError("Both good_count and total_count must be numbers.")

        # Check if total_count is not zero
        if self.total_count == 0:
            raise ValueError("total_count cannot be zero.")

        # Calculate and return the quality aspect of OEE
        return self.good_count / self.total_count

    def calculate_availability(self):

        # Check if run_time and total_time are numbers
        if not isinstance(self.run_time, (int, float)) or not isinstance(self.total_time, (int, float)):
            raise ValueError("Both run_time and total_time must be numbers.")

        # Check if total_time is not zero
        if self.total_time == 0:
            raise ValueError("total_time cannot be zero.")

        # Calculate and return the availability aspect of OEE
        return self.run_time / self.total_time

    def calculate_performance(self):

        # Check if total_count and target_count are numbers
        if not isinstance(self.total_count, (int, float)) or not isinstance(self.target_count, (int, float)):
            raise ValueError("Both total_count and target_count must be numbers.")

        # Check if target_count is not zero
        if self.target_count == 0:
            raise ValueError("target_count cannot be zero.")

        # Calculate and return the performance aspect of OEE
        return self.total_count / self.target_count

    def calculate_oee(self):

        try:

            # Calculate the quality, availability, and performance aspects of OEE
            quality = self.calculate_quality()
            availability = self.calculate_availability()
            performance = self.calculate_performance()

            # Calculate and return the overall OEE
            return quality * availability * performance

        except ValueError as ve:
            raise ValueError("Error calculating OEE: " + str(ve))

        except Exception as e:
            raise Exception("Unexpected error calculating OEE: " + str(e))

    @staticmethod
    def get_connection():
        if OeeModel.connection_pool is None:
            OeeModel.connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
        return OeeModel.connection_pool.getconn()

    @staticmethod
    def release_connection(connection):
        if OeeModel.connection_pool is not None:
            OeeModel.connection_pool.putconn(connection)

    @staticmethod
    def handle_db_error(e):
        logger.error(f"Database error occurred: {e}")
        raise Exception("An error occurred while accessing the database.")

    @staticmethod
    @contextmanager
    def get_db_connection():
        conn = OeeModel.get_connection()
        try:
            yield conn
        finally:
            if conn is not None:
                OeeModel.release_connection(conn)

    @staticmethod
    def _parse_timestamp(timestamp_str):
        # Define the accepted input formats for timestamp
        input_formats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S %Z', '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S.%fZ']

        # Iterate over input formats and try to parse the timestamp
        for fmt in input_formats:
            try:
                dt = datetime.strptime(timestamp_str, fmt)
                dt = dt.replace(tzinfo=timezone.utc)  # Assuming timestamps are in UTC timezone
                return dt
            except ValueError:
                pass

        # Raise an exception if the timestamp cannot be parsed
        raise ValueError("Invalid timestamp format. Please provide a valid timestamp string.")

    # def insert_oee_data(self):

    @staticmethod
    def get_latest_oee(object_type, object_id):
        try:
            query = """
            SELECT availability, performance, quality, oee, good_count, total_count, run_time, total_time, target_count, time
            FROM oee_data
            WHERE object_type = %s AND object_id = %s
            ORDER BY time DESC
            LIMIT 1
            """

            with OeeModel.get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (object_type, object_id))
                    result = cur.fetchone()
                    if result:
                        columns = ['availability', 'performance', 'quality', 'oee', 'good_count', 'total_count',
                                   'run_time',
                                   'total_time', 'target_count', 'timestamp']
                        return dict(zip(columns, result))
                    else:
                        return {}

        except psycopg2.DatabaseError as e:
            OeeModel.handle_db_error(e)
        except Exception as e:
            logger.error(f"Failed to fetch latest OEE data: {e}")
            raise Exception("An error occurred while fetching latest OEE data.")

    @staticmethod
    def get_oee_by_date_range(object_type, object_id, start_date, end_date):
        try:
            # Convert start_date and end_date to timestamps in 'YYYY-MM-DD HH:MM:SS TZ' format
            start_timestamp = OeeModel._parse_timestamp(start_date)
            end_timestamp = OeeModel._parse_timestamp(end_date)

            query = """
                SELECT avg(availability) AS availability,
                       avg(performance) AS performance,
                       avg(quality) AS quality,
                       avg(oee) AS oee,
                       sum(good_count) AS total_good_count,
                       sum(total_count) AS total_total_count,
                       sum(run_time) AS total_run_time,
                       sum(total_time) AS total_total_time,
                       sum(target_count) AS total_target_count,
                       time_bucket('1 day', time) AS timestamp,
                       min(time) AS start_time,
                       max(time) AS end_time
                FROM oee_data
                WHERE object_type = %s AND object_id = %s
                  AND time >= %s AND time <= %s
                GROUP BY timestamp
                ORDER BY timestamp
            """

            with OeeModel.get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (object_type, object_id, start_timestamp, end_timestamp))
                    results = cur.fetchall()

                    columns = ['availability', 'performance', 'quality', 'oee', 'total_good_count', 'total_total_count',
                               'total_run_time', 'total_total_time', 'total_target_count', 'timestamp', 'start_time',
                               'end_time']
                    oee_list = [dict(zip(columns, row)) for row in results]

                    return oee_list

        except psycopg2.DatabaseError as e:
            OeeModel.handle_db_error(e)
        except Exception as e:
            logger.error(f"Failed to fetch OEE data by date range: {e}")
            raise Exception("An error occurred while fetching OEE data by date range.")
