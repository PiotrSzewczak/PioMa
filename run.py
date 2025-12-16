import pandas as pd
from lib.geocode import geocode_addresses
from lib.db import Database
from config.config import get_database
from dotenv import load_dotenv

addresses_df = pd.read_csv('addresses.csv', sep=';')


# jedno wywołanie geokodowania
addresses_df = geocode_addresses(addresses_df)

print(addresses_df)

# wrzucenie do bazy
db = get_database()
db.insert_dataframe('pioma_proj.apartments_geocoded', addresses_df)

input("Press Enter to close")
