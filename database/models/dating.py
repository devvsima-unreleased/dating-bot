from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class DatingProfileModel(BaseModel):
    __tablename__ = "dating_profiles"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    find_gender: Mapped[str] = mapped_column(String(20), nullable=False)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"), nullable=False)
    photo: Mapped[str] = mapped_column(String(255), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    instagram: Mapped[str] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="dating_profile")  # type: ignore
    location: Mapped["LocationModel"] = relationship("LocationModel")  # type: ignore
    goals: Mapped[list["DatingGoalModel"]] = relationship(
        "DatingGoalModel", secondary="dating_profile_goals", back_populates="profiles"
    )

    __table_args__ = (
        CheckConstraint("gender IN ('male', 'female')", name="gender_check"),
        CheckConstraint("find_gender IN ('male', 'female', 'all')", name="find_gender_check"),
    )


class DatingGoalModel(BaseModel):
    __tablename__ = "dating_goals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    profiles: Mapped[list["DatingProfileModel"]] = relationship(
        "DatingProfileModel", secondary="dating_profile_goals", back_populates="goals"
    )
