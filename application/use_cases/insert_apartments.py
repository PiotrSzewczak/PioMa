import logging
from dataclasses import dataclass
from typing import List, Optional

import pandas as pd

from domain.entities import Apartment
from infrastructure.repositories.apartment_repository import ApartmentRepository
from services.geocoder import GeocoderService

logger = logging.getLogger(__name__)


@dataclass
class InsertResult:
    """Result of insert operation."""

    inserted_count: int
    skipped_count: int
    failed_count: int


class InsertApartmentsUseCase:
    """Use case for inserting apartments with geocoding and deduplication."""

    def __init__(self, repository: ApartmentRepository, geocoder: GeocoderService):
        self.repository = repository
        self.geocoder = geocoder

    def execute(self, apartments_data: List[dict]) -> InsertResult:
        """
        Insert apartments from list of dictionaries.

        Args:
            apartments_data: List of dicts with keys: apartment_id, city, street, house_nr

        Returns:
            InsertResult with counts of inserted, skipped, and failed records.
        """
        inserted = 0
        skipped = 0
        failed = 0
        apartments_to_insert: List[Apartment] = []

        for data in apartments_data:
            apartment_id = data.get("apartment_id", "")

            if not apartment_id:
                logger.warning("Skipping record without apartment_id")
                failed += 1
                continue

            # Check for duplicates
            if self.repository.exists(apartment_id):
                logger.info(f"Apartment {apartment_id} already exists, skipping")
                skipped += 1
                continue

            try:
                apartment = self._create_apartment_with_geocoding(data)
                apartments_to_insert.append(apartment)
            except Exception as e:
                logger.error(f"Failed to process apartment {apartment_id}: {e}")
                failed += 1

        # Batch insert
        if apartments_to_insert:
            inserted = self.repository.insert_many(apartments_to_insert)
            logger.info(f"Inserted {inserted} apartments")

        return InsertResult(
            inserted_count=inserted,
            skipped_count=skipped,
            failed_count=failed,
        )

    def execute_from_dataframe(self, df: pd.DataFrame) -> InsertResult:
        """
        Insert apartments from pandas DataFrame.

        Expected columns: apartment_id, city, street, house_nr
        Optional columns: latitude, longitude (if present, geocoding is skipped)
        """
        apartments_data = df.to_dict("records")
        return self.execute(apartments_data)

    def _create_apartment_with_geocoding(self, data: dict) -> Apartment:
        """Create apartment entity, geocoding if coordinates not provided."""
        apartment_id = data.get("apartment_id", "")
        city = data.get("city", "")
        street = data.get("street", "")
        house_nr = data.get("house_nr", "")

        # Check if coordinates are already provided
        lat = data.get("latitude")
        lon = data.get("longitude")

        # Geocode if coordinates not provided or invalid
        if lat is None or lon is None or lat == 0.0 or lon == 0.0:
            full_address = f"{city} {street} {house_nr}".strip()
            logger.info(f"Geocoding address: {full_address}")
            lat, lon = self.geocoder.geocode(full_address)

            if lat is None or lon is None:
                logger.warning(f"Geocoding failed for: {full_address}")
                lat, lon = 0.0, 0.0

        return Apartment.create(
            apartment_id=apartment_id,
            city=city,
            street=street,
            house_nr=house_nr,
            latitude=lat,
            longitude=lon,
        )
