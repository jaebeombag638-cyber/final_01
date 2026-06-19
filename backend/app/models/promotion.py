from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class PromotionProduct(Base):
    __tablename__ = "promotion_products"

    promo_product_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    promo_product_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)
    placement: Mapped[str] = mapped_column(String(100), nullable=False)
    slot_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    promotions: Mapped[list["Promotion"]] = relationship(back_populates="product")


class Promotion(Base):
    __tablename__ = "promotions"

    promotion_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    promo_product_id: Mapped[int] = mapped_column(Integer, ForeignKey("promotion_products.promo_product_id", ondelete="RESTRICT"), nullable=False)
    service_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("services.service_id", ondelete="CASCADE"), nullable=False)
    used_points: Mapped[int] = mapped_column(Integer, nullable=False)
    start_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default="now()")
    end_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default="진행중")

    product: Mapped["PromotionProduct"] = relationship(back_populates="promotions")
    service: Mapped["Service"] = relationship(back_populates="promotions")  # noqa: F821
