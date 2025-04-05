from sqlalchemy import Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class LocationModel(BaseModel, AsyncAttrs):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Обратная связь с ServiceProfileModel
    service_profiles: Mapped[list["ServiceProfileModel"]] = relationship(
        "ServiceProfileModel", back_populates="location"
    )
