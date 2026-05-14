from sqlalchemy import Column, Integer, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class UserVehicleRating(Base):
    __tablename__ = "user_vehicle_ratings"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.vehicle_id"), nullable=False)

    performance = Column(Float, nullable=True)
    size = Column(Float, nullable=True)
    economy = Column(Float, nullable=True)
    practicality = Column(Float, nullable=True)
    exoticness = Column(Float, nullable=True)
    engagement = Column(Float, nullable=True)

    vehicle = relationship("Vehicle")
    user = relationship("User")

    __table_args__ = (
        UniqueConstraint("user_id", "vehicle_id", name="uq_user_vehicle_axes"),
    )
