from pydantic import BaseModel, Field, UUID4
from typing import List, Optional
from datetime import date
from typing import List, Union


class CibleCreate(BaseModel):
    age: List[int]
    genre: str
    campaign_id: UUID4


class CibleCreateInCampaign(BaseModel):
    age: List[int]
    genre: str


class Cible(CibleCreate):
    id: UUID4

    class ConfigDict:
        from_attributes = True
