import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AssetModel:
    connection_pool = None

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.parent_id = kwargs.get('parent_id')
        self.object_type = kwargs.get('asset_type')

    @staticmethod
    def get_connection():
        if AssetModel.connection_pool is None:
            AssetModel.connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
        return AssetModel.connection_pool.getconn()

    @staticmethod
    def release_connection(connection):
        if AssetModel.connection_pool is not None:
            AssetModel.connection_pool.putconn(connection)

    @staticmethod
    def execute_query(query, params):
        conn = None
        try:
            conn = AssetModel.get_connection()
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()

                if 'RETURNING' in query:
                    result = cur.fetchone()
                    if result and len(result) > 0:
                        return result

        except (Exception, psycopg2.DatabaseError) as e:
            logger.error(e)
            if conn is not None:
                conn.rollback()  # rollback the transaction on errors
            raise Exception(f"Database query execution failed. {e}")

        finally:
            if conn is not None:
                AssetModel.release_connection(conn)

    @staticmethod
    def fetch_one(query, params):
        conn = None
        try:
            conn = AssetModel.get_connection()
            with conn.cursor() as cur:
                cur.execute(query, params)
                result = cur.fetchone()
                if result is None:
                    raise Exception("No data found.")
                columns = [col[0] for col in cur.description]
                data = dict(zip(columns, result))
                return data
        except (Exception, psycopg2.DatabaseError) as e:
            logger.error(e)
            if conn is not None:
                conn.rollback()  # rollback the transaction on errors
            raise Exception(f"Failed to fetch data from database. {e}")

        finally:
            if conn is not None:
                AssetModel.release_connection(conn)

    @staticmethod
    def fetch_all(query, params=None):
        conn = None
        try:
            conn = AssetModel.get_connection()
            with conn.cursor() as cur:
                if params is None:
                    cur.execute(query)
                else:
                    cur.execute(query, params)

                result = cur.fetchall()
                if len(result) == 0:
                    raise ValueError("No data found.")
                columns = [col[0] for col in cur.description]
                data = [dict(zip(columns, res)) for res in result]
                return data
        except (Exception, psycopg2.DatabaseError) as e:
            logger.error(e)
            if conn is not None:
                conn.rollback()  # rollback the transaction on errors
            raise Exception(f"Failed to fetch data from database. {e}")

        finally:
            if conn is not None:
                AssetModel.release_connection(conn)


class EnterpriseModel(AssetModel):
    def create(self):
        try:
            result = self.execute_query(
                "INSERT INTO obj_enterprises (name, description, object_type) VALUES (%s, %s, %s) RETURNING id",
                (self.name, self.description, 4)
            )

            if result:
                logger.info(result[0])
                asset = EnterpriseModel.get(self, result[0])
                return asset
            else:
                raise Exception("Failed to retrieve the ID of the inserted row")

        except Exception as e:
            raise Exception(f"Failed to create enterprise. {e}")

    def get(self, asset_id):
        try:
            data = self.fetch_one(
                """
                SELECT id, name, description, parent_id, object_type 
                FROM obj_enterprises 
                WHERE id = %s AND NOT deprecated
                """,
                (asset_id,)
            )
            if data:
                self.__dict__.update(data)
                return self
            else:
                raise ValueError("No data found for the given asset ID.")
        except Exception as e:
            raise Exception(f"Failed to get enterprise. {e}")

    def update(self, asset_id):
        try:
            self.execute_query(
                "UPDATE obj_enterprises SET name = %s, description = %s WHERE id = %s AND NOT deprecated",
                (self.name, self.description, asset_id)
            )
            asset = EnterpriseModel.get(self, asset_id)
            return asset

        except Exception as e:
            raise Exception(f"Failed to update enterprise. {e}")

    def delete(self):
        try:
            self.execute_query(
                "UPDATE obj_enterprises SET deprecated = true WHERE id = %s AND NOT deprecated",
                (self.id,)
            )
        except Exception as e:
            raise Exception(f"Failed to delete enterprise. {e}")

    @staticmethod
    def get_all():
        try:
            query = """
                SELECT id, name, description, parent_id, object_type
                FROM obj_enterprises
                WHERE NOT deprecated
            """
            data = AssetModel.fetch_all(query)
            enterprises = [EnterpriseModel(**item) for item in data]
            return enterprises
        except Exception as e:
            raise Exception(f"Failed to get all enterprises. {e}")


class SiteModel(AssetModel):
    def create(self):
        try:
            query = """
                INSERT INTO obj_sites (name, description, parent_id, object_type) 
                VALUES (%s, %s, %s, %s) 
                RETURNING id
            """
            result = self.execute_query(query, (self.name, self.description, self.parent_id, 3))

            if result:
                logger.info(result[0])
                asset = SiteModel.get(self, result[0])
                return asset
            else:
                raise Exception("Failed to retrieve the ID of the inserted row")

        except Exception as e:
            raise Exception(f"Failed to create site. {e}")

    def get(self, asset_id):
        try:
            data = self.fetch_one("""
                SELECT id, name, description, parent_id, object_type 
                FROM obj_sites 
                WHERE id = %s AND NOT deprecated
                """, (asset_id,)
            )
            if data:
                self.__dict__.update(data)
                return self
            else:
                raise ValueError("No data found for the given asset ID.")
        except Exception as e:
            raise Exception(f"Failed to get site. {e}")

    def update(self, asset_id):
        try:
            self.execute_query(
                "UPDATE obj_sites SET name = %s, description = %s WHERE id = %s AND NOT deprecated",
                (self.name, self.description, asset_id)
            )
            asset = SiteModel.get(self, asset_id)
            return asset

        except Exception as e:
            raise Exception(f"Failed to update site. {e}")

    def delete(self):
        try:
            self.execute_query(
                "UPDATE obj_sites SET deprecated = true WHERE id = %s AND NOT deprecated",
                (self.id,)
            )
        except Exception as e:
            raise Exception(f"Failed to delete site. {e}")

    @staticmethod
    def get_all():
        try:
            query = """
                SELECT id, name, description, parent_id, object_type
                FROM obj_sites
                WHERE NOT deprecated
            """
            data = AssetModel.fetch_all(query)
            enterprises = [SiteModel(**item) for item in data]
            return enterprises
        except Exception as e:
            raise Exception(f"Failed to get all sites. {e}")


class AreaModel(AssetModel):
    def create(self):
        try:
            query = """
                INSERT INTO obj_areas (name, description, parent_id, object_type) 
                VALUES (%s, %s, %s, %s) 
                RETURNING id
            """
            result = self.execute_query(query, (self.name, self.description, self.parent_id, 3))

            if result:
                logger.info(result[0])
                asset = AreaModel.get(self, result[0])
                return asset
            else:
                raise Exception("Failed to retrieve the ID of the inserted row")

        except Exception as e:
            raise Exception(f"Failed to create area. {e}")

    def get(self, asset_id):
        try:
            data = self.fetch_one("""
                SELECT id, name, description, parent_id, object_type 
                FROM obj_areas 
                WHERE id = %s AND NOT deprecated
                """, (asset_id,)
            )
            if data:
                self.__dict__.update(data)
                return self
            else:
                raise ValueError("No data found for the given asset ID.")
        except Exception as e:
            raise Exception(f"Failed to get area. {e}")

    def update(self, asset_id):
        try:
            self.execute_query(
                "UPDATE obj_areas SET name = %s, description = %s WHERE id = %s AND NOT deprecated",
                (self.name, self.description, asset_id)
            )
            asset = AreaModel.get(self, asset_id)
            return asset

        except Exception as e:
            raise Exception(f"Failed to update area. {e}")

    def delete(self):
        try:
            self.execute_query(
                "UPDATE obj_areas SET deprecated = true WHERE id = %s AND NOT deprecated",
                (self.id,)
            )
        except Exception as e:
            raise Exception(f"Failed to delete area. {e}")

    @staticmethod
    def get_all():
        try:
            query = """
                SELECT id, name, description, parent_id, object_type
                FROM obj_areas
                WHERE NOT deprecated
            """
            data = AssetModel.fetch_all(query)
            enterprises = [AreaModel(**item) for item in data]
            return enterprises
        except Exception as e:
            raise Exception(f"Failed to get all areas. {e}")
