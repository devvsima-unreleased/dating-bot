from sqlalchemy import Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class LocationModel(BaseModel, AsyncAttrs):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    offers: Mapped[list["OfferModel"]] = relationship("OfferModel", back_populates="location")  # type: ignore
