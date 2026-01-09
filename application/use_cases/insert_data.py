import logging

import pandas as pd
import psycopg2
import psycopg2.extras

from lib.db import Database
from lib.geocode import Geocoder
from domain.entities import Apartment

logger = logging.getLogger(__name__)


class DataInserter:
    def __init__(self, db: Database, geocoder: Geocoder):
        self.db = db
        self.geocoder = geocoder

    def insert_data(self, df: pd.DataFrame, table_name: str):
        try:
            apartment_list = []
            for _, row in df.iterrows():
                logger.info(f"Processing row: {row.to_dict()}")
                apartment_id = row.get("apartment_id")
                if not self.db.is_apartment_exist(apartment_id):
                    city = row.get("city", "")
                    street = row.get("street", "")
                    house_number = row.get("house_number", "")  # czytamy kolumnę z DF
                    concatted_address = f"{city} {street} {house_number}"
                    logger.info(f"Concatenated address: {concatted_address}")
                    if concatted_address:
                        lat, lon = self.geocoder.geocode_address(concatted_address)
                        if lat is None or lon is None:
                            logger.warning(
                                f"Geocoding failed for address: {concatted_address}"
                            )
                        apartment = Apartment(
                            apartment_id=apartment_id,
                            city=city,
                            street=street,
                            house_number=house_number,
                            full_address=concatted_address,
                            latitude=lat if lat is not None else 0.0,
                            longitude=lon if lon is not None else 0.0,
                        )
                        apartment_list.append(apartment)
            df_to_insert = pd.DataFrame(apartment_list)
            if not df_to_insert.empty:
                # mapujemy nazwę pola obiektu na nazwę kolumny w bazie
                df_to_insert = df_to_insert.rename(columns={"house_number": "house_nr"})
                self.db.insert_dataframe(table_name, df_to_insert)
        except Exception as e:
            print(f"Error inserting data: {e}")
