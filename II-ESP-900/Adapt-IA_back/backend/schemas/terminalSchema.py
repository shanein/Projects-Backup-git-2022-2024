from pydantic import BaseModel, Field, UUID4
from typing import List, Optional
from datetime import datetime


class TerminalCreate(BaseModel):
    place_type: str = Field(
        ..., description="Type de lieu (ex: Café, Restaurant, etc.)"
    )
    name: str = Field(..., description="Nom du lieu")
    description: str = Field(..., description="Description du lieu")
    localisation: str = Field(..., description="Adresse du lieu")
    lat: float = Field(..., description="Latitude du lieu")
    long: float = Field(..., description="Longitude du lieu")
    week_schedule: dict = Field(..., description="Horaire d'ouverture du lieu")
    start_date: str = Field(
        ..., description="Date souhaitée de début d'activité de la borne"
    )
    unavailable_dates: List[dict] = Field(
        ..., description="Dates d'indisponibilité du lieu"
    )

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "place_type": "Café",
                "name": "Café Central",
                "description": "Un café confortable au centre-ville",
                "localisation": "123 Rue Principale, Ville",
                "lat": 45.123456,
                "long": -73.123456,
                "start_date": "2021-01-01",
                "week_schedule": {
                    "lundi": {"opening": "08:00", "closing": "18:00"},
                    "mardi": {"opening": "08:00", "closing": "18:00"},
                    "mercredi": {"opening": "08:00", "closing": "18:00"},
                    "jeudi": {"opening": "08:00", "closing": "18:00"},
                    "vendredi": {"opening": "08:00", "closing": "18:00"},
                    "samedi": {"opening": "08:00", "closing": "18:00"},
                    "dimanche": {"opening": "08:00", "closing": "18:00"},
                },
                "unavailable_dates": [
                    {"start_date": "2023-12-24", "end_date": "2023-12-26"},
                    {"start_date": "2024-01-01", "end_date": "2024-01-01"},
                ],
            }
        }


class Terminal(TerminalCreate):
    id: UUID4
    distributor_id: UUID4
    is_active: bool
    secret_key: Optional[str]
    last_update: Optional[datetime]
    ip_address: Optional[str]

    class ConfigDict:
        from_attributes = True


class TerminalUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    place_type: Optional[str] = None
    unavailable_dates: Optional[List[dict]] = None
