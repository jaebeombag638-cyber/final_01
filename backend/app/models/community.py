from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CommunityPost(Base):
    __tablename__ = "community_posts"

    post_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    post_type: Mapped[str] = mapped_column(String(20), nullable=False)
    post_title: Mapped[str] = mapped_column(String(200), nullable=False)
    post_content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default="now()")
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    view_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    user: Mapped["User"] = relationship(back_populates="posts")  # noqa: F821
    comments: Mapped[list["CommunityComment"]] = relationship(back_populates="post", cascade="all, delete-orphan")


class CommunityComment(Base):
    __tablename__ = "community_comments"

    comment_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("community_posts.post_id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default="now()")
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    post: Mapped["CommunityPost"] = relationship(back_populates="comments")
    user: Mapped["User"] = relationship(back_populates="comments")  # noqa: F821
