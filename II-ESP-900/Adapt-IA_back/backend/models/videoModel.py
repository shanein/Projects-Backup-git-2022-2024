from sqlalchemy import Column, Integer, String, UUID, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from database.database import Base, engine  # Assuming you have a 'database' module
from models.Campaign_Terminal import Campaign


class Video(Base):
    __tablename__ = "video"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    path = Column(String)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="videos")


# Create the tables in the database
Base.metadata.create_all(bind=engine)
