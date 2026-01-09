import psycopg2
import psycopg2.extras
import pandas as pd


class Database:
    def __init__(self, db_host, db_port, db_name, db_user, db_password):
        self.connection_params = {
            "host": db_host,
            "port": db_port,
            "database": db_name,
            "user": db_user,
            "password": db_password,
        }

    def connect(self):
        return psycopg2.connect(**self.connection_params)

    def _fetch_raw(self, table_name: str):
        query = f"SELECT * FROM {table_name};"
        try:
            conn = self.connect()

            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(query)
            records = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]

            cursor.close()
            conn.close()

            return records, col_names
        except Exception as e:
            return [], []

    def fetch_as_dataframe(self, table_name: str) -> pd.DataFrame:
        records, col_names = self._fetch_raw(table_name)
        if records:
            df = pd.DataFrame(records, columns=col_names)
            return df
        else:
            return pd.DataFrame()

    def insert_dataframe(self, table_name: str, df: pd.DataFrame):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            columns = [f'"{col}"' for col in df.columns]
            values = [tuple(x) for x in df.to_numpy()]
            insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s"
            psycopg2.extras.execute_values(cursor, insert_query, values)
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def is_apartment_exist(self, apartment_id: str) -> bool:
        """
        Check if an apartment with the given apartment_id exists in the database.
        Args:
            apartment_id: The unique identifier of the apartment.
        Returns:
            True if the apartment exists, False otherwise.
        """
        conn = self.connect()
        cursor = conn.cursor()
        try:
            query = (
                "SELECT 1 FROM pioma_proj.apartments WHERE apartment_id = %s LIMIT 1;"
            )
            cursor.execute(query, (apartment_id,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            conn.close()

    def exists(self, table: str, **filters):
        conn = self.connect()
        cursor = conn.cursor()

        try:
            conditions = []
            values = []

            for key, value in filters.items():
                conditions.append(f"{key} = %s")
                values.append(value)

            where_clause = " AND ".join(conditions)

            query = f"SELECT 1 FROM {table} WHERE {where_clause} LIMIT 1"
            cursor.execute(query, values)

            return cursor.fetchone() is not None
        finally:
            cursor.close()
            conn.close()

            # Aktualizacja danych z uruchomieniem skryptu na geokoding ++++
