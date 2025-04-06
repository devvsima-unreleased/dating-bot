from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

offer_service_types = Table(
    "offer_service_types",
    BaseModel.metadata,
    Column("offer_id", ForeignKey("offers.user_id", ondelete="CASCADE"), primary_key=True),
    Column("offer_type_id", ForeignKey("offer_types.id", ondelete="CASCADE"), primary_key=True),
)


class OfferTypeModel(BaseModel):
    __tablename__ = "offer_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    offers: Mapped[list["OfferModel"]] = relationship(
        "OfferModel", secondary="offer_service_types", back_populates="offer_types"
    )


class OfferModel(BaseModel):
    __tablename__ = "offers"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    location_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("locations.id", ondelete="SET NULL"), nullable=True
    )
    photo: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    instagram: Mapped[str] = mapped_column(String(200), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    # Связь с UserModel
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="offer")  # type: ignore

    # Связь с LocationModel
    location: Mapped["LocationModel"] = relationship("LocationModel", back_populates="offers")  # type: ignore

    # Связь с ServiceTypeModel через offer_service_types
    offer_types: Mapped[list["OfferTypeModel"]] = relationship(
        "OfferTypeModel", secondary=offer_service_types, back_populates="offers"
    )
