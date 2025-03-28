from sqlalchemy import BigInteger, Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .location import service_profile_location_association


class ServiceProfileModel(BaseModel):
    __tablename__ = "service_profiles"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    photo: Mapped[str] = mapped_column(String(255), nullable=False)
    instagram: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Связь с услугами
    services: Mapped[list["ServiceModel"]] = relationship(
        "ServiceModel", back_populates="profile", cascade="all, delete-orphan"
    )

    # Связь с локациями
    locations: Mapped[list["LocationModel"]] = relationship(  # type: ignore
        "LocationModel",
        secondary=service_profile_location_association,
        back_populates="service_profiles",
    )

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="service_profile")  # type: ignore


class ServiceModel(BaseModel):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    profile_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("service_profiles.user_id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    profile: Mapped["ServiceProfileModel"] = relationship(
        "ServiceProfileModel", back_populates="services"
    )
