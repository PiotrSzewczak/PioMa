from typing import TypedDict
import pandas as pd


class BaseModel(TypedDict):
    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([self])


class Apartment(BaseModel):
    apartment_id: str
    city: str
    street: str
    house_number: str
    full_address: str
    latitude: float
    longitude: float
