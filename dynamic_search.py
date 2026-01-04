import psycopg2
import psycopg2.extras
import pandas as pd
import re
from lib.db import Database


def dynamic_search(db: Database, searched_value: str) -> pd.DataFrame:
    """
    Execute a fuzzy search against the apartments table using a whitespace-tolerant pattern.

    Args:
        db: Database client responsible for providing psycopg2 connections.
        searched_value: Raw address fragment supplied by the caller.

    Returns:
        A DataFrame containing matching apartment rows, or an empty DataFrame when no criteria is provided.
    """

    def escape_like(fragment: str) -> str:
        """Escape single quotes to keep literal ILIKE patterns valid."""
        return fragment.replace("'", "''")

    # Normalize whitespace to align user input with how addresses are stored.
    normalized_value = re.sub(r"\s+", " ", (searched_value or "")).strip()
    if not normalized_value:
        return pd.DataFrame()

    # Build a wildcard pattern that tolerates arbitrary characters between tokens.
    tokens = normalized_value.split(" ")
    wildcard_pattern = f"%{'%'.join(tokens)}%"
    escaped_wildcard = escape_like(wildcard_pattern)

    # Compose literal clauses per current requirement (no parameter binding).
    conditions = [f"a.full_address ILIKE '{escaped_wildcard}'"]
    if len(tokens) > 1:
        token_conditions = " AND ".join(
            [f"a.full_address ILIKE '%{escape_like(token)}%'" for token in tokens]
        )
        conditions.append(f"({token_conditions})")

    where_clause = " OR ".join(conditions)

    # Execute the dynamically constructed search and return the resulting DataFrame.
    conn = db.connect()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        query = f"""
            SELECT *
            FROM pioma_proj.apartments AS a
            WHERE {where_clause};
        """
        cursor.execute(query)
        records = cursor.fetchall()

        col_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(records, columns=col_names)

        return df

    finally:
        cursor.close()
        conn.close()
