from pydantic import BaseModel, Field, UUID4
from typing import List, Optional


class Target(BaseModel):
    age: List[str]
    gender: List[str]
    clothing_Style: List[str]
    clothing_Color: List[str]


class Config:
    orm_mode = True
