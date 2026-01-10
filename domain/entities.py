from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Apartment:
    """Domain entity representing an apartment."""

    apartment_id: str
    city: str
    street: str
    house_nr: str
    full_address: str
    latitude: float
    longitude: float

    def to_dict(self) -> dict:
        """Convert entity to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Apartment":
        """Create Apartment from dictionary."""
        return cls(
            apartment_id=data.get("apartment_id", ""),
            city=data.get("city", ""),
            street=data.get("street", ""),
            house_nr=data.get("house_nr", ""),
            full_address=data.get("full_address", ""),
            latitude=data.get("latitude", 0.0),
            longitude=data.get("longitude", 0.0),
        )

    @classmethod
    def create(
        cls,
        apartment_id: str,
        city: str,
        street: str,
        house_nr: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
    ) -> "Apartment":
        """Factory method to create Apartment with auto-generated full_address."""
        full_address = f"{city} {street} {house_nr}".strip()
        return cls(
            apartment_id=apartment_id,
            city=city,
            street=street,
            house_nr=house_nr,
            full_address=full_address,
            latitude=latitude if latitude is not None else 0.0,
            longitude=longitude if longitude is not None else 0.0,
        )
