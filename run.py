import pandas as pd
from lib.geocode import geocode_addresses
from lib.db import Database
from config.config import get_database
from search import search_apartments
from dotenv import load_dotenv
from dynamic_search import dynamic_search
from lib.typesofdata import Apartment

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
db = get_database()
apt = Apartment(
    street="Marszałkowska",
    house_nr="10",
    city="Warszawa"
)

#print(dynamic_search(db, "warszawa"))
print(db.exists("pioma_proj.apartments", **apt))
print(db.fetch_as_dataframe("pioma_proj.apartments"))
print(geocode_addresses(apt))







