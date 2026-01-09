import pandas as pd
from geopy.geocoders import Nominatim


class Geocoder:
    """
    A simple geocoder class that uses Nominatim to convert addresses into geographic coordinates.
    """

    def __init__(self):
        self.geolocator = Nominatim(user_agent="myGeocoder")

    def geocode_address(self, address: str):
        """
        Geocode the given address string into latitude and longitude.
        Args:
            address: The address string to geocode.
        Returns:
            A tuple of (latitude, longitude) if found, otherwise (None, None).
        """
        location = self.geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
