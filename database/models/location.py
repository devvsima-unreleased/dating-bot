from sqlalchemy import BigInteger, Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

service_profile_location_association = Table(
    "service_profile_location_association",
    BaseModel.metadata,
    Column(
        "profile_id",
        BigInteger,
        ForeignKey("service_profiles.user_id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "location_id", BigInteger, ForeignKey("locations.id", ondelete="CASCADE"), primary_key=True
    ),
)


class LocationModel(BaseModel):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)

    # Связь с профилями услуг (многие ко многим)
    service_profiles: Mapped[list["ServiceProfileModel"]] = relationship(  # type: ignore
        "ServiceProfileModel",
        secondary=service_profile_location_association,
        back_populates="locations",
    )
