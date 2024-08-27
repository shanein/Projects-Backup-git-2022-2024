from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, UUID, ARRAY
from sqlalchemy.orm import relationship
from database.database import Base
import uuid
from enum import Enum
from sqlalchemy.types import JSON


class Cible(Base):
    __tablename__ = "cible"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    age = Column(ARRAY(Integer))
    genre = Column(String)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="cible")
