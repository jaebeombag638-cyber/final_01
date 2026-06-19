from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class PointLog(Base):
    __tablename__ = "point_logs"

    log_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    current_points: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default="now()")

    user: Mapped["User"] = relationship(back_populates="point_logs")  # noqa: F821


class Attendance(Base):
    __tablename__ = "attendance"

    attend_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    attended_date: Mapped[str] = mapped_column(String(10), nullable=False)
    streak_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="1")

    user: Mapped["User"] = relationship(back_populates="attendances")  # noqa: F821
