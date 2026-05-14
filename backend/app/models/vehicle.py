from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import relationship
from app.database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    vehicle_id = Column(Integer, primary_key=True)

    vehicle_name = Column(String, nullable=True)
    production_year = Column(Integer, nullable=True)

    performance_score = Column(Float, nullable=False)
    size_score = Column(Float, nullable=False)
    economy_score = Column(Float, nullable=False)
    practicality_score = Column(Float, nullable=False)
    exoticness_score = Column(Float, nullable=False)
    engagement_score = Column(Float, nullable=False)

    raw = relationship("VehicleRaw", back_populates="vehicle", uselist=False)
