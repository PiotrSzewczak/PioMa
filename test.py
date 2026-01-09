import logging

import pandas as pd

from config.config import get_database
from lib.geocode import Geocoder
from application.use_cases.dynamic_search import DynamicSearch
from application.use_cases.insert_data import DataInserter


def main():

    logging.basicConfig(level=logging.INFO)

    addresses_df = pd.read_csv("addresses.csv", sep=";")
    addresses_df = addresses_df.rename(
        columns={
            "ID_new": "apartment_id",
            "Ulica": "street",
            "Numer domu": "house_nr",  # ujednolicone z kolumną w DB
            "Miasto": "city",
            "Concat": "full_address",
            "Longitude": "longitude",
            "Latitude": "latitude",
        }
    )

    db = get_database()
    table_name = "pioma_proj.apartments"  # <- bez końcowej spacji

    geocoder = Geocoder()
    inserter = DataInserter(db, geocoder)
    inserter.insert_data(addresses_df, table_name)


if __name__ == "__main__":
    main()
