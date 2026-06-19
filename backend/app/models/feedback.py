from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Feedback(Base):
    __tablename__ = "feedbacks"

    feedback_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    service_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("services.service_id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default="now()")
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default="now()")
    char_count: Mapped[int | None] = mapped_column(Integer, nullable=True)

    service: Mapped["Service"] = relationship(back_populates="feedbacks")  # noqa: F821
    user: Mapped["User"] = relationship(back_populates="feedbacks")  # noqa: F821
