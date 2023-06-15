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
    table_name = None  # Add a class attribute for the table name

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
            raise Exception(f"Failed to create {self.table_name}. {e}")

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
            else:
                raise ValueError("No data found for the given asset ID.")
        except Exception as e:
            raise Exception(f"Failed to get {self.table_name}. {e}")

    def update(self, asset_id):
        try:
            self.execute_query(
                f"UPDATE {self.table_name} SET name = %s, description = %s WHERE id = %s AND NOT deprecated",
                (self.name, self.description, asset_id)
            )
            asset = self.get(asset_id)
            return asset

        except Exception as e:
            raise Exception(f"Failed to update {self.table_name}. {e}")

    def delete(self):
        try:
            self.execute_query(
                f"UPDATE {self.table_name} SET deprecated = true WHERE id = %s AND NOT deprecated",
                (self.id,)
            )
        except Exception as e:
            raise Exception(f"Failed to delete {self.table_name}. {e}")

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
            raise Exception(f"Failed to get all {self.table_name}. {e}")


class EnterpriseModel(AssetModel):
    table_name = 'obj_enterprises'
    object_name = 'enterprise'
    object_type = 4

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_type = EnterpriseModel.object_type

    def create(self):
        return super().create()

    def get(self, asset_id):
        return super().get(asset_id)

    def update(self, asset_id):
        return super().update(asset_id)

    def delete(self):
        return super().delete()

    def get_all(self):
        return super().get_all()


class SiteModel(AssetModel):
    path = 'enterprise'
    object_name = 'site'
    object_type = 3

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_type = SiteModel.object_type

    def create(self):
        return super().create()

    def get(self, asset_id):
        return super().get(asset_id)

    def update(self, asset_id):
        return super().update(asset_id)

    def delete(self):
        return super().delete()

    def get_all(self):
        return super().get_all()


class AreaModel(AssetModel):
    table_name = 'obj_areas'
    object_name = 'area'
    object_type = 2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_type = AreaModel.object_type

    def create(self):
        return super().create()

    def get(self, asset_id):
        return super().get(asset_id)

    def update(self, asset_id):
        return super().update(asset_id)

    def delete(self):
        return super().delete()

    def get_all(self):
        return super().get_all()


class LineModel(AssetModel):
    table_name = 'obj_lines'
    object_name = 'line'
    object_type = 2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_type = LineModel.object_type

    def create(self):
        return super().create()

    def get(self, asset_id):
        return super().get(asset_id)

    def update(self, asset_id):
        return super().update(asset_id)

    def delete(self):
        return super().delete()

    def get_all(self):
        return super().get_all()


class CellModel(AssetModel):
    table_name = 'obj_cells'
    object_name = 'cell'
    object_type = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_type = CellModel.object_type

    def create(self):
        return super().create()

    def get(self, asset_id):
        return super().get(asset_id)

    def update(self, asset_id):
        return super().update(asset_id)

    def delete(self):
        return super().delete()

    def get_all(self):
        return super().get_all()
