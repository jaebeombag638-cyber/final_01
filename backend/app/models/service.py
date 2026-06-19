from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Service(Base):
    __tablename__ = "services"

    service_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.category_id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    summary: Mapped[str] = mapped_column(String(300), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    service_url: Mapped[str] = mapped_column(Text, nullable=False)
    thumbnail_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default="대기중")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default="now()")
    view_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    user: Mapped["User"] = relationship(back_populates="services")  # noqa: F821
    category: Mapped["Category"] = relationship(back_populates="services")  # noqa: F821
    feedbacks: Mapped[list["Feedback"]] = relationship(back_populates="service", cascade="all, delete-orphan")  # noqa: F821
    promotions: Mapped[list["Promotion"]] = relationship(back_populates="service", cascade="all, delete-orphan")  # noqa: F821
    entry_logs: Mapped[list["ServiceEntryLog"]] = relationship(back_populates="service")  # noqa: F821


class ServiceEntryLog(Base):
    __tablename__ = "service_entry_logs"

    log_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("users.user_id"), nullable=True)
    session_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    service_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("services.service_id"), nullable=False)
    promo_product_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("promotion_products.promo_product_id"), nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default="now()")
    source_page: Mapped[str | None] = mapped_column(String(100), nullable=True)

    service: Mapped["Service"] = relationship(back_populates="entry_logs")
