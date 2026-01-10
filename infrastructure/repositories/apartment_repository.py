import re
from typing import List, Optional

import psycopg2.extras

from domain.entities import Apartment
from infrastructure.database import Database


class ApartmentRepository:
    """Repository for apartment database operations."""

    TABLE_NAME = "pioma_proj.apartments"

    def __init__(self, db: Database):
        self.db = db

    def exists(self, apartment_id: str) -> bool:
        """Check if an apartment with the given ID exists."""
        query = f"SELECT 1 FROM {self.TABLE_NAME} WHERE apartment_id = %s LIMIT 1;"
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (apartment_id,))
            return cursor.fetchone() is not None

    def insert(self, apartment: Apartment) -> None:
        """Insert a single apartment into the database."""
        query = f"""
            INSERT INTO {self.TABLE_NAME} 
            (apartment_id, city, street, house_nr, full_address, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        with self.db.get_cursor() as cursor:
            cursor.execute(
                query,
                (
                    apartment.apartment_id,
                    apartment.city,
                    apartment.street,
                    apartment.house_nr,
                    apartment.full_address,
                    apartment.latitude,
                    apartment.longitude,
                ),
            )

    def insert_many(self, apartments: List[Apartment]) -> int:
        """Insert multiple apartments. Returns count of inserted records."""
        if not apartments:
            return 0

        query = f"""
            INSERT INTO {self.TABLE_NAME} 
            (apartment_id, city, street, house_nr, full_address, latitude, longitude)
            VALUES %s;
        """
        values = [
            (
                apt.apartment_id,
                apt.city,
                apt.street,
                apt.house_nr,
                apt.full_address,
                apt.latitude,
                apt.longitude,
            )
            for apt in apartments
        ]

        with self.db.get_cursor() as cursor:
            psycopg2.extras.execute_values(cursor, query, values)
            return len(apartments)

    def get_by_id(self, apartment_id: str) -> Optional[Apartment]:
        """Fetch a single apartment by ID."""
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE apartment_id = %s LIMIT 1;"
        with self.db.get_cursor(dict_cursor=True) as cursor:
            cursor.execute(query, (apartment_id,))
            row = cursor.fetchone()
            if row:
                return Apartment.from_dict(dict(row))
            return None

    def get_by_ids(self, apartment_ids: List[str]) -> List[Apartment]:
        """Fetch apartments by list of IDs."""
        if not apartment_ids:
            return []

        placeholders = ",".join(["%s"] * len(apartment_ids))
        query = (
            f"SELECT * FROM {self.TABLE_NAME} WHERE apartment_id IN ({placeholders});"
        )

        with self.db.get_cursor(dict_cursor=True) as cursor:
            cursor.execute(query, tuple(apartment_ids))
            rows = cursor.fetchall()
            return [Apartment.from_dict(dict(row)) for row in rows]

    def get_all(self) -> List[Apartment]:
        """Fetch all apartments."""
        query = f"SELECT * FROM {self.TABLE_NAME};"
        with self.db.get_cursor(dict_cursor=True) as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return [Apartment.from_dict(dict(row)) for row in rows]

    def search_by_address(self, search_value: str, limit: int = 10) -> List[Apartment]:
        """
        Execute a fuzzy search against the apartments table.
        Returns list of matching Apartment entities.

        Args:
            search_value: Address fragment to search for.
            limit: Maximum number of results to return (default 10).
        """
        normalized_value = re.sub(r"\s+", " ", (search_value or "")).strip()
        if not normalized_value:
            return []

        tokens = normalized_value.split(" ")

        # Build parameterized query for safety
        wildcard_pattern = f"%{'%'.join(tokens)}%"

        conditions = ["full_address ILIKE %s"]
        params: list = [wildcard_pattern]

        if len(tokens) > 1:
            token_conditions = " AND ".join(["full_address ILIKE %s"] * len(tokens))
            conditions.append(f"({token_conditions})")
            params.extend([f"%{token}%" for token in tokens])

        where_clause = " OR ".join(conditions)
        params.append(limit)
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE {where_clause} LIMIT %s;"

        with self.db.get_cursor(dict_cursor=True) as cursor:
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            return [Apartment.from_dict(dict(row)) for row in rows]

    def find_nearest(self, full_address: str, limit: int = 3) -> List[Apartment]:
        """Find the nearest apartments to the given address."""
        query = f"""
            SELECT a.apartment_id, a.city, a.street, a.house_nr, 
                   a.full_address, a.latitude, a.longitude,
                   ST_Distance(
                       ST_SetSRID(ST_MakePoint(a.longitude, a.latitude), 4326),
                       ST_SetSRID(ST_MakePoint(t.longitude, t.latitude), 4326)
                   ) AS distance_m
            FROM {self.TABLE_NAME} AS a
            JOIN {self.TABLE_NAME} AS t ON t.full_address = %s
            WHERE a.full_address <> t.full_address
            ORDER BY distance_m ASC
            LIMIT %s;
        """
        with self.db.get_cursor(dict_cursor=True) as cursor:
            cursor.execute(query, (full_address, limit))
            rows = cursor.fetchall()
            return [Apartment.from_dict(dict(row)) for row in rows]
