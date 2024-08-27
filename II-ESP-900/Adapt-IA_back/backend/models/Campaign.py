from sqlalchemy import ARRAY, Column, Integer, String, Date, ForeignKey, Boolean, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Table
from database.database import Base, engine
import uuid
from models.Cible import Cible
from sqlalchemy.types import JSON


class Campaign(Base):
    __tablename__ = "campaign"
    __table_args__ = {"extend_existing": True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    budget = Column(Integer)
    is_smart = Column(Boolean)
    address = Column(String)
    postal_code = Column(String)
    is_active = Column(Boolean, default=True)
    is_valid = Column(Boolean, default=True)
    advertiser_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    advertiser = relationship("User", back_populates="campaigns")
    cible = relationship("Cible", back_populates="campaign")
    videos = relationship(
        "Video", back_populates="campaign"
    )  # Change 'video' to 'videos'


Base.metadata.create_all(bind=engine)
