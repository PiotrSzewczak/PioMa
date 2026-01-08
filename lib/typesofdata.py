from typing import TypedDict
import pandas as pd

class BaseModel(TypedDict):
    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([self])

class Apartment(BaseModel):
    street: str
    house_number: str
    # apartament_number: str = None
    city: str

# Zastanawiam się czy nie lepiej tego używać jeśli chodzi o obiekty z bazy danych jakby w sensie nie wiem czy to na wstępie //
#nie robię źle ale tak to naprawdę możemy tak wypisywać nie wiem coś tak myśle XD