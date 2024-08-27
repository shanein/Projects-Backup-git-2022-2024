from pydantic import BaseModel, Field, UUID4
from typing import List
from schemas.videoSchema import VideoResponse


class CampaignInfo(BaseModel):
    info: str
    videos: List[VideoResponse]


class ClientConfig(BaseModel):
    version: str
    campaign: CampaignInfo
