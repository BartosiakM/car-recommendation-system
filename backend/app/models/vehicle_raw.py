from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.database import Base

class VehicleRaw(Base):
    __tablename__ = "vehicle_raw"

    vehicle_id = Column(Integer, ForeignKey("vehicles.vehicle_id", ondelete="CASCADE"), primary_key=True)

    data = Column(JSONB, nullable=False)

    vehicle = relationship("Vehicle", back_populates="raw", uselist=False)
