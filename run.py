import pandas as pd
from lib.geocode import geocode_addresses
from lib.db import Database
from config.config import get_database
from dotenv import load_dotenv

addresses_df = pd.read_csv('addresses.csv', sep=';')


# jedno wywołanie geokodowania
addresses_df = geocode_addresses(addresses_df)
addresses_df = addresses_df.rename(columns={
    "ID_new": "id",
    "Ulica": "street",
    "Numer domu": "house_nr",
    "Miasto": "city",
    "Concat": "full_address",
    "Longitude": "longitude",
    "Latitude": "latitude"
})
# podgląd wyników
#
print(addresses_df)

# wrzucenie do bazy
db = get_database()
db.insert_dataframe('pioma_proj.apartments', addresses_df)



