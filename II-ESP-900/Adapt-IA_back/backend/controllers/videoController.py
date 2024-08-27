from sqlalchemy.orm import Session
import logging  # Import Python's logging module
from schemas.videoSchema import VideoCreate, VideoResponse
from models.videoModel import Video
from models.Campaign_Terminal import Campaign
from uuid import UUID, uuid4
from fastapi import HTTPException, UploadFile, File, logger
from decouple import config
from cloudinary.uploader import upload
import cloudinary
import cloudinary.uploader


cloudinary.config(
    cloud_name=config("CLOUD_NAME"),
    api_key=config("API_KEY"),
    api_secret=config("API_SECRET"),
)

# Set up logging configuration
logging.basicConfig(level=logging.ERROR)  # Set the logging level to ERROR


def upload_to_cloudinary(file: UploadFile) -> str:
    try:
        # Configure Cloudinary (replace placeholders with actual credentials)
        cloudinary.config(
            cloud_name=config(("CLOUD_NAME")),
            api_key=config(("API_KEY")),
            api_secret=config(("API_SECRET")),
        )

        # Upload the video file to Cloudinary
        upload_result = upload(file.file)
        return upload_result["secure_url"]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error uploading to Cloudinary"
        ) from e


def create_video(file: UploadFile, campaign_id: str, db: Session) -> VideoResponse:
    try:
        # Check if the campaign_id exists in the Campaign table
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign ID does not exist")
        upload_result = cloudinary.uploader.upload(file.file, resource_type="video")

        # Create a new Video entry in the database with the Cloudinary URL and campaign_id
        new_video = Video(path=upload_result["secure_url"], campaign_id=campaign_id)
        db.add(new_video)
        db.commit()
        db.refresh(new_video)

        return VideoResponse(
            id=new_video.id, path=new_video.path, campaign_id=new_video.campaign_id
        )

    except HTTPException:
        raise  # Re-raise HTTPExceptions as they are already properly handled

    except Exception as e:
        logger.error(
            f"Error creating video: {str(e)}"
        )  # Log the specific error details
        raise HTTPException(
            status_code=500,
            detail="Error creating video. Check server logs for more details.",
        ) from e


def get_videos_by_campaign_id(campaign_id: str, db: Session):
    return db.query(Video).filter(Video.campaign_id == campaign_id).all()


def process_video_upload(
    file: UploadFile, campaign_id: str, db: Session
) -> VideoResponse:
    try:
        video_url = upload_to_cloudinary(file)
        print(video_url)
        return create_video(video_url, campaign_id, db)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error processing video upload"
        ) from e


def get_video_by_id(video_id: int, db: Session):
    result = db.query(Video).filter(Video.id == video_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Video is not found")
    return result


def get_videos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Video).offset(skip).limit(limit).all()


def update_video(video_id: int, video: VideoCreate, db: Session):
    try:
        db_video = db.query(Video).filter(Video.id == video_id).first()
        if db_video:
            for key, value in video.dict().items():
                setattr(db_video, key, value)
            db.commit()
            return db_video  # Return the updated video object
        else:
            raise HTTPException(status_code=404, detail="Video not found")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def delete_video(video_id: str, db: Session):
    # Query the database to check if the video with the specified UUID exists
    db_video = db.query(Video).filter(Video.id == video_id).first()

    if not db_video:
        # Return False if the video doesn't exist
        return False

    # Delete the video and commit the changes
    db.query(Video).filter(Video.id == video_id).delete()
    db.commit()

    # Return True indicating successful deletion
    return True


def delete_videos_by_video_url(video_url: str, db: Session):
    # Query the database to check if the video with the specified URL exists
    db_video = db.query(Video).filter(Video.path == video_url).first()

    if not db_video:
        # Return False if the video doesn't exist
        return False

    # Delete the video and commit the changes
    db.query(Video).filter(Video.path == video_url).delete()
    db.commit()

    # Return True indicating successful deletion
    return True
