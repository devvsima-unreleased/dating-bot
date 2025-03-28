from sqlalchemy import BigInteger, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    language: Mapped[str] = mapped_column(String(10), nullable=False, default="en")
    created_at: Mapped[str] = mapped_column(String(50), nullable=False)
    referral: Mapped[int] = mapped_column(Integer, default=0)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)

    # Связь с профилем знакомств
    dating_profile: Mapped["DatingProfileModel"] = relationship(  # type: ignore
        "DatingProfileModel", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    # Связь с профилем услуг
    service_profile: Mapped["ServiceProfileModel"] = relationship(  # type: ignore
        "ServiceProfileModel", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    # Связь с матчами (отправленные и полученные)
    sent_matches: Mapped[list["MatchModel"]] = relationship(  # type: ignore
        "MatchModel", foreign_keys="[MatchModel.sender_id]", back_populates="sender"
    )
    received_matches: Mapped[list["MatchModel"]] = relationship(  # type: ignore
        "MatchModel", foreign_keys="[MatchModel.receiver_id]", back_populates="receiver"
    )
