import psycopg2
import psycopg2.extras
import pandas as pd

class Database:
    def __init__(self, db_host, db_port, db_name, db_user, db_password):
        self.connection_params = {
                    'host': db_host,
                    'port': db_port,
                    'database': db_name,
                    'user': db_user,
                    'password': db_password
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