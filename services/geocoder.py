from typing import Tuple, Optional
from geopy.geocoders import Nominatim


class GeocoderService:
    """Service for geocoding addresses to coordinates."""

    def __init__(self, user_agent: str = "apartment_geocoder"):
        self.geolocator = Nominatim(user_agent=user_agent)

    def geocode(self, address: str) -> Tuple[Optional[float], Optional[float]]:
        """
        Geocode an address string into latitude and longitude.

        Args:
            address: The address string to geocode.

        Returns:
            A tuple of (latitude, longitude) if found, otherwise (None, None).
        """
        if not address or not address.strip():
            return None, None

        try:
            location = self.geolocator.geocode(address, timeout=10)
            if location:
                return location.latitude, location.longitude
        except Exception:
            pass

        return None, None
