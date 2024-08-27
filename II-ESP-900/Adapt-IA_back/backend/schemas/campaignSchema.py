from fastapi import File, UploadFile
from pydantic import BaseModel, Field, UUID4
from typing import List, Optional
from datetime import date
from schemas.cibleSchema import *


class CampaignCreate(BaseModel):
    name: str
    description: str
    start_date: str
    end_date: str
    budget: Optional[int]
    is_smart: bool
    address: str
    postal_code: str
    cible: Optional[List[CibleCreateInCampaign]] = []
    terminals: Optional[List[str]] = []


class CampaignNew(BaseModel):
    id: Optional[UUID4] = None
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    budget: Optional[int] = None
    is_smart: Optional[bool] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    cible: Optional[List[CibleCreateInCampaign]] = None


class CampaignUpdate(BaseModel):
    id: Optional[UUID4] = None
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    budget: Optional[int] = None
    is_smart: Optional[bool] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    cible: Optional[List[CibleCreateInCampaign]] = None


class CampaignUpdateIsValid(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    budget: Optional[int] = None


class BodyCreateNewCampaignWithVideo(BaseModel):
    campaign: CampaignCreate
    video_file: UploadFile = File(...)


class Campaign(CampaignCreate):
    id: Optional[UUID4] = None
    advertiser_id: UUID4
    videoUrl: str
    cibles: List[Cible] = []
    is_active: bool
    is_valid: bool

    class ConfigDict:
        from_attributes = True
