from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID, uuid4
from controllers.videoController import (
    create_video,
    process_video_upload,
    get_videos_by_campaign_id,
    delete_video,
    delete_videos_by_video_url,
)
from schemas.videoSchema import VideoCreate, VideoResponse
from controllers.authController import get_current_user_from_token
from models.videoModel import Video
from models.Campaign_Terminal import Campaign
from uuid import UUID, uuid4

from decouple import config


router = APIRouter(tags=["Video"])


@router.post("/videos/", response_model=VideoResponse)
def create_video_endpoint(
    campaign_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    if file.content_type.startswith("video"):
        # Upload the video file to Cloudinary
        # upload_result = cloudinary.uploader.upload(file.file, resource_type="video")
        # Process the upload_result as needed
        return create_video(file, campaign_id, db)
    else:
        raise HTTPException(status_code=400, detail="Please upload a valid video file")


# @router.post("/upload_video/")
# async def upload_video(file: UploadFile = File(...)):
#     if file.content_type.startswith("video"):
#         # Upload the video file to Cloudinary
#         upload_result = cloudinary.uploader.upload(file.file, resource_type="video")
#         # Process the upload_result as needed
#         return {"status": "success", "public_id": upload_result["public_id"]}
#     else:
#         return {"status": "failed", "message": "Please upload a valid video file"}


@router.get("/video/{campaign_id}", response_model=VideoResponse)
def get_videos_by_campaign_id_endpoint(campaign_id: str, db: Session = Depends(get_db)):
    try:
        campaign_uuid = UUID(campaign_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    db_campaign = db.query(Video).filter(Video.campaign_id == campaign_uuid).first()
    if db_campaign is None:
        # Raise a 404 Not Found error if the campaign doesn't exist
        raise HTTPException(status_code=404, detail="Campaign not found")

    # Return the videos for the specified campaign
    return db_campaign


@router.get("/videos/", response_model=List[VideoResponse])
def read_videos(db: Session = Depends(get_db)):
    videos = db.query(Video).all()
    return videos


@router.get("/video_by_id/{video_id}", response_model=VideoResponse)
def read_video(
    video_id: str,
    db: Session = Depends(get_db),
    # user=Depends(get_current_user_from_token),
):
    try:
        video_uuid = UUID(video_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    db_video = db.query(Video).filter(Video.id == video_uuid).first()
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")

    return db_video


@router.delete("/videos/{video_id}", response_model=str)
def delete_videof(
    video_id: UUID,  # Assuming you want to use UUIDs for video IDs
    db: Session = Depends(get_db),
    # user=Depends(get_current_user_from_token),
):
    deleted_video = delete_video(db=db, video_id=video_id)
    if not deleted_video:
        raise HTTPException(status_code=404, detail="Video not found")

    return "Video deleted successfully"


@router.delete("/videourl", response_model=str)
def delete_video_by_url(
    video_url: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    deleted_video = delete_videos_by_video_url(db=db, video_url=video_url)
    if not deleted_video:
        raise HTTPException(status_code=404, detail="Video not found")

    return "Video deleted successfully"
