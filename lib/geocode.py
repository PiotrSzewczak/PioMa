import pandas as pd
from geopy.geocoders import Nominatim

def geocode_addresses(input_csv: str) -> pd.DataFrame:
    geolocator = Nominatim(user_agent="myGeocoder")
    
    input_csv['latitude'] = None
    input_csv['longitude'] = None

    for idx, row in input_csv.iterrows():
        address = row['Concat']
        location = geolocator.geocode(address, timeout=25)

        if location:
            input_csv.at[idx, 'latitude'] = location.latitude
            input_csv.at[idx, 'longitude'] = location.longitude
        else:
            input_csv.at[idx, 'latitude'] = None
            input_csv.at[idx, 'longitude'] = None

    return input_csv