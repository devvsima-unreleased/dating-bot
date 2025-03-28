from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class MatchModel(BaseModel):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sender_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    receiver_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    message: Mapped[str] = mapped_column(Text, nullable=True)

    sender: Mapped["UserModel"] = relationship(  # type: ignore
        "UserModel", foreign_keys=[sender_id], back_populates="sent_matches"
    )
    receiver: Mapped["UserModel"] = relationship(  # type: ignore
        "UserModel", foreign_keys=[receiver_id], back_populates="received_matches"
    )

    __table_args__ = (
        CheckConstraint(
            "sender_id != receiver_id", name="check_self_match"
        ),  # Запрещает совпадение пользователя с самим собой
    )
