from pydantic import BaseModel, UUID4


class VideoCreate(BaseModel):
    path: str
    campaign_id: UUID4


class VideoResponse(BaseModel):
    id: UUID4
    path: str
    campaign_id: UUID4


class Video(BaseModel):
    path: str
    campaign_id: UUID4

    class Config:
        orm_mode = True
