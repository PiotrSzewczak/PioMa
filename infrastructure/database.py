import psycopg2
import psycopg2.extras
from contextlib import contextmanager
from typing import Generator, Any


class Database:
    """Low-level database connection manager."""

    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        self.connection_params = {
            "host": host,
            "port": port,
            "database": database,
            "user": user,
            "password": password,
        }

    def connect(self) -> psycopg2.extensions.connection:
        """Create and return a new database connection."""
        return psycopg2.connect(**self.connection_params)

    @contextmanager
    def get_connection(self) -> Generator[psycopg2.extensions.connection, None, None]:
        """Context manager for database connections."""
        conn = self.connect()
        try:
            yield conn
        finally:
            conn.close()

    @contextmanager
    def get_cursor(
        self, dict_cursor: bool = False
    ) -> Generator[psycopg2.extensions.cursor, None, None]:
        """Context manager for database cursors with automatic commit."""
        with self.get_connection() as conn:
            cursor_factory = psycopg2.extras.DictCursor if dict_cursor else None
            cursor = conn.cursor(cursor_factory=cursor_factory)
            try:
                yield cursor
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                cursor.close()
