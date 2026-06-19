from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    role: Mapped[str] = mapped_column(String(20), nullable=False, server_default="user")
    current_points: Mapped[int] = mapped_column(Integer, nullable=False, server_default="500")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default="now()")
    oauth_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    follower_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    following_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    interests: Mapped[list["UserInterest"]] = relationship(back_populates="user", cascade="all, delete-orphan")  # noqa: F821
    services: Mapped[list["Service"]] = relationship(back_populates="user")  # noqa: F821
    feedbacks: Mapped[list["Feedback"]] = relationship(back_populates="user")  # noqa: F821
    point_logs: Mapped[list["PointLog"]] = relationship(back_populates="user")  # noqa: F821
    attendances: Mapped[list["Attendance"]] = relationship(back_populates="user", cascade="all, delete-orphan")  # noqa: F821
    posts: Mapped[list["CommunityPost"]] = relationship(back_populates="user")  # noqa: F821
    comments: Mapped[list["CommunityComment"]] = relationship(back_populates="user")  # noqa: F821
    reports: Mapped[list["Report"]] = relationship(back_populates="user")  # noqa: F821
    following: Mapped[list["UserFollow"]] = relationship(foreign_keys="UserFollow.follower_id", back_populates="follower")  # noqa: F821
    followers: Mapped[list["UserFollow"]] = relationship(foreign_keys="UserFollow.following_id", back_populates="following_user")  # noqa: F821


class UserInterest(Base):
    __tablename__ = "user_interests"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.category_id", ondelete="CASCADE"), primary_key=True)

    user: Mapped["User"] = relationship(back_populates="interests")
    category: Mapped["Category"] = relationship(back_populates="user_interests")  # noqa: F821


class UserFollow(Base):
    __tablename__ = "user_follows"
    __table_args__ = (UniqueConstraint("follower_id", "following_id"),)

    follow_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    follower_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    following_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default="ACTIVE")
    created_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, server_default="now()")
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    follower: Mapped["User"] = relationship(foreign_keys=[follower_id], back_populates="following")
    following_user: Mapped["User"] = relationship(foreign_keys=[following_id], back_populates="followers")
