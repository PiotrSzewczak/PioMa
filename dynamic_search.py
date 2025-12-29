import psycopg2
import psycopg2.extras
import pandas as pd

def dynamic_search(db, searched_value):
    conn = db.connect()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        query = """
            SELECT *
            FROM pioma_proj.apartments AS a
            WHERE a.full_address ILIKE %s;
        """
        param = f"%{searched_value}%"

        cursor.execute(query, (param,))
        records = cursor.fetchall()

        col_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(records, columns=col_names)

        return df

    finally:
        cursor.close()
        conn.close()
