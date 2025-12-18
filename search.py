import psycopg2
import psycopg2.extras
import pandas as pd

def search_apartments(db, apart: str) -> pd.DataFrame:
    """
    Find the 3 nearest apartments to the given full_address and return them as a DataFrame.
    """
    conn = db.connect() # establish a new connection
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) # use DictCursor for better column access
    try:
        query = """
            SELECT a.id, 
            a.full_address,
            ST_Distance(
              ST_SetSRID(ST_MakePoint(a.longitude, a.latitude), 4326),
              ST_SetSRID(ST_MakePoint(t.longitude, t.latitude), 4326)
            ) AS distance_m
            FROM pioma_proj.apartments AS a
            JOIN pioma_proj.apartments AS t
               ON t.full_address = %s
               WHERE a.full_address <> t.full_address
            ORDER BY distance_m ASC
            LIMIT 3;
        """ 
        cursor.execute(query, [apart])
        records = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]

        df = pd.DataFrame(records, columns=col_names)
        return df
    finally:
        cursor.close()
        conn.close()
