from sqlalchemy import BigInteger, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

ROLES = {
    0: "banned",
    1: "user",
    2: "sponsor",
    3: "moderator",
    4: "admin",
    5: "owner",
}  # not currently in use


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(70), nullable=True)
    language: Mapped[str] = mapped_column(String(10), default="en")
    referral: Mapped[int] = mapped_column(Integer, default=0)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)

    profile: Mapped["ProfileModel"] = relationship(  # type: ignore
        "ProfileModel", uselist=False, back_populates="user"
    )
    offer: Mapped["OfferModel"] = relationship("OfferModel", back_populates="user")  # type: ignore
