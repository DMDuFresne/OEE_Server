import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv
from contextlib import contextmanager
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AssetModel:
    connection_pool = None
    table_name = None
    parent_table_name = None
    child_table_name = None
    object_name = 'asset'
    object_type = None

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.parent_id = kwargs.get('parent_id')
        self.object_type = kwargs.get('asset_type')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "parent_id": self.parent_id,
            "object_type": self.object_type,
        }

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
    def handle_db_error(e):
        logger.error(f"Database error occurred. {e}")
        if 'no results to fetch' in str(e):
            raise Exception("No results to fetch. Please check your query.")
        else:
            raise Exception("An error occurred while fetching data from the database.")

    @staticmethod
    @contextmanager
    def get_db_connection():
        conn = AssetModel.get_connection()
        try:
            yield conn
        finally:
            if conn is not None:
                AssetModel.release_connection(conn)

    @staticmethod
    def execute_query(query, params):
        try:
            with AssetModel.get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    conn.commit()

                    if 'RETURNING' in query:
                        result = cur.fetchone()
                        if result and len(result) > 0:
                            return result

        except psycopg2.DatabaseError as e:
            AssetModel.handle_db_error(e)
        except Exception as e:
            logger.error(f"Database query execution failed. {e}")
            raise Exception("An error occurred while executing the database query.")

    @staticmethod
    def fetch_one(query, params):
        try:
            with AssetModel.get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    result = cur.fetchone()
                    if result is None:
                        result = []
                    columns = [col[0] for col in cur.description]
                    data = dict(zip(columns, result))
                    return data

        except psycopg2.DatabaseError as e:
            AssetModel.handle_db_error(e)
        except Exception as e:
            logger.error(f"Failed to fetch data from database. {e}")
            raise Exception("An error occurred while fetching data from the database.")

    @staticmethod
    def fetch_all(query, params=None):
        try:
            with AssetModel.get_db_connection() as conn:
                with conn.cursor() as cur:
                    if params is None:
                        cur.execute(query)
                    else:
                        cur.execute(query, params)

                    result = cur.fetchall()
                    if len(result) == 0:
                        result = []
                    columns = [col[0] for col in cur.description]
                    data = [dict(zip(columns, res)) for res in result]
                    return data

        except psycopg2.DatabaseError as e:
            AssetModel.handle_db_error(e)
        except Exception as e:
            logger.error(f"Failed to fetch data from database. {e}")
            raise Exception("An error occurred while fetching data from the database.")

    def create(self):

        try:
            query = f"""
                INSERT INTO {self.table_name} (name, description, parent_id, object_type) 
                VALUES (%s, %s, %s, %s) 
                RETURNING id
            """
            result = self.execute_query(query, (self.name, self.description, self.parent_id, self.object_type))

            if result:
                logger.info(result[0])
                asset = self.get(result[0])
                return asset
            else:
                raise Exception("Failed to retrieve the ID of the inserted row")

        except Exception as e:
            logger.error(f"Failed to create {self.object_name}. {e}")
            raise Exception(f"An error occurred while creating the {self.object_name}.")

    def get(self, asset_id):
        try:
            data = self.fetch_one(f"""
                SELECT id, name, description, parent_id, object_type 
                FROM {self.table_name} 
                WHERE id = %s AND NOT deprecated
                """, (asset_id,)
            )
            if data:
                self.__dict__.update(data)
                return self
        except Exception as e:
            logger.error(f"Failed to get  {self.object_name}. {e}")
            raise Exception(f"An error occurred while fetching the {self.object_name}.")

    def update(self, asset_id):
        try:
            self.execute_query(
                f"UPDATE {self.table_name} SET name = %s, description = %s WHERE id = %s AND NOT deprecated",
                (self.name, self.description, asset_id)
            )
            asset = self.get(asset_id)
            return asset

        except Exception as e:
            logger.error(f"Failed to update {self.object_name}. {e}")
            raise Exception(f"An error occurred while updating the {self.object_name}.")

    def delete(self):
        try:
            self.execute_query(
                f"UPDATE {self.table_name} SET deprecated = true WHERE id = %s AND NOT deprecated",
                (self.id,)
            )
        except Exception as e:
            logger.error(f"Failed to delete {self.object_name}. {e}")
            raise Exception(f"An error occurred while deleting the {self.object_name}.")

    def get_all(self):
        try:
            query = f"""
                SELECT id, name, description, parent_id, object_type
                FROM {self.table_name}
                WHERE NOT deprecated
            """
            data = self.fetch_all(query)
            assets = [AssetModel(**item) for item in data]
            return assets
        except Exception as e:
            logger.error(f"Failed to get all {self.object_name}. {e}")
            raise Exception(f"An error occurred while fetching all {self.object_name}.")

    def get_children(self, asset_id):

        try:

            query = f"""
                SELECT id, name, description, parent_id, object_type
                FROM {self.child_table_name}
                WHERE parent_id = {asset_id} AND NOT deprecated
            """
            data = self.fetch_all(query)
            assets = [AssetModel(**item) for item in data]
            return assets
        except Exception as e:
            logger.error(f"Failed to get children of the {self.object_name}. {e}")
            raise Exception(f"An error occurred while fetching children of the {self.object_name}.")

    def get_parent(self, asset_id):

        try:

            asset = self.get(asset_id)
            parent_id = asset.parent_id

            query = f"""
                SELECT id, name, description, parent_id, object_type
                FROM {self.parent_table_name}
                WHERE id = {parent_id} AND NOT deprecated
            """
            data = self.fetch_all(query)
            assets = [AssetModel(**item) for item in data]
            return assets
        except Exception as e:
            logger.error(f"Failed to get the parent of the {self.object_name}. {e}")
            raise Exception(f"An error occurred while fetching the parent of the {self.object_name}.")


class EnterpriseModel(AssetModel):
    parent_table_name = None
    table_name = 'obj_enterprises'
    child_table_name = 'obj_sites'
    object_name = 'enterprise'
    object_type = 4

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_type = EnterpriseModel.object_type


class SiteModel(AssetModel):
    parent_table_name = 'obj_enterprises'
    table_name = 'obj_sites'
    child_table_name = 'obj_areas'
    object_name = 'site'
    object_type = 3

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_type = SiteModel.object_type


class AreaModel(AssetModel):
    parent_table_name = 'obj_sites'
    table_name = 'obj_areas'
    child_table_name = 'obj_lines'
    object_name = 'area'
    object_type = 2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_type = AreaModel.object_type


class LineModel(AssetModel):
    parent_table_name = 'obj_areas'
    table_name = 'obj_lines'
    child_table_name = 'obj_cells'
    object_name = 'line'
    object_type = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_type = LineModel.object_type


class CellModel(AssetModel):
    parent_table_name = 'obj_lines'
    table_name = 'obj_cells'
    child_table_name = None
    object_name = 'cell'
    object_type = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_type = CellModel.object_type
