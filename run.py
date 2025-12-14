import pandas as pd
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="myGeocoder")

addresses_df = pd.read_csv('addresses.csv', sep=';')

for idx, row in addresses_df.iterrows():
    address = row['Concat']
    location = geolocator.geocode(address, timeout=25)

    print(location.latitude, location.longitude)  # For debugging purposes
    if location:
        addresses_df.at[idx, 'latitude'] = location.latitude
        addresses_df.at[idx, 'longitude'] = location.longitude
    else:
        addresses_df.at[idx, 'latitude'] = None
        addresses_df.at[idx, 'longitude'] = None

    df = pd.read_csv('addresses.csv', sep=';')
    print(df)
    input("Press Enter to close")