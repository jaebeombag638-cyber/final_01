"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-06-19

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("category_id", sa.Integer(), sa.Identity(), nullable=False),
        sa.Column("category_name", sa.String(50), nullable=False),
        sa.PrimaryKeyConstraint("category_id"),
        sa.UniqueConstraint("category_name"),
    )

    op.create_table(
        "users",
        sa.Column("user_id", sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column("nickname", sa.String(50), nullable=False),
        sa.Column("role", sa.String(20), nullable=False, server_default="user"),
        sa.Column("current_points", sa.Integer(), nullable=False, server_default="500"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("oauth_id", sa.String(255), nullable=False),
        sa.Column("last_login", sa.DateTime(), nullable=True),
        sa.Column("follower_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("following_count", sa.Integer(), nullable=False, server_default="0"),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("nickname"),
        sa.UniqueConstraint("oauth_id"),
        sa.CheckConstraint("current_points >= 0", name="ck_users_current_points"),
    )

    op.create_table(
        "user_interests",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["category_id"], ["categories.category_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "category_id"),
    )

    op.create_table(
        "attendance",
        sa.Column("attend_id", sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("attended_date", sa.String(10), nullable=False),
        sa.Column("streak_count", sa.Integer(), nullable=False, server_default="1"),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("attend_id"),
        sa.UniqueConstraint("user_id", "attended_date", name="uq_attendance_user_date"),
    )

    op.create_table(
        "services",
        sa.Column("service_id", sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("summary", sa.String(300), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("service_url", sa.Text(), nullable=False),
        sa.Column("thumbnail_url", sa.Text(), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="대기중"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("view_count", sa.Integer(), nullable=False, server_default="0"),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["category_id"], ["categories.category_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("service_id"),
        sa.CheckConstraint("status IN ('대기중', '활성', '차단')", name="ck_services_status"),
    )

    op.create_table(
        "feedbacks",
        sa.Column("feedback_id", sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column("service_id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("char_count", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["service_id"], ["services.service_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("feedback_id"),
    )

    op.create_table(
        "promotion_products",
        sa.Column("promo_product_id", sa.Integer(), sa.Identity(), nullable=False),
        sa.Column("promo_product_name", sa.String(100), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("duration_days", sa.Integer(), nullable=False),
        sa.Column("placement", sa.String(100), nullable=False),
        sa.Column("slot_limit", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("promo_product_id"),
        sa.UniqueConstraint("promo_product_name"),
        sa.CheckConstraint("price > 0", name="ck_promotion_products_price"),
        sa.CheckConstraint("duration_days > 0", name="ck_promotion_products_duration"),
        sa.CheckConstraint("slot_limit > 0", name="ck_promotion_products_slot"),
    )

    op.create_table(
        "promotions",
        sa.Column("promotion_id", sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column("promo_product_id", sa.Integer(), nullable=False),
        sa.Column("service_id", sa.BigInteger(), nullable=False),
        sa.Column("used_points", sa.Integer(), nullable=False),
        sa.Column("start_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("end_at", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="진행중"),
        sa.ForeignKeyConstraint(["promo_product_id"], ["promotion_products.promo_product_id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["service_id"], ["services.service_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("promotion_id"),
        sa.CheckConstraint("used_points >= 0", name="ck_promotions_used_points"),
        sa.CheckConstraint("status IN ('진행중', '종료됨')", name="ck_promotions_status"),
    )

    op.create_table(
        "point_logs",
        sa.Column("log_id", sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("current_points", sa.Integer(), nullable=False),
        sa.Column("reason", sa.String(255), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("log_id"),
        sa.CheckConstraint("amount <> 0", name="ck_point_logs_amount"),
        sa.CheckConstraint("current_points >= 0", name="ck_point_logs_current_points"),
    )

    op.create_table(
        "community_posts",
        sa.Column("post_id", sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("post_type", sa.String(20), nullable=False),
        sa.Column("post_title", sa.String(200), nullable=False),
        sa.Column("post_content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("view_count", sa.Integer(), nullable=False, server_default="0"),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("post_id"),
        sa.CheckConstraint("post_type IN ('자유게시판', '팀구하기', '문의')", name="ck_community_posts_type"),
    )

    op.create_table(
        "community_comments",
        sa.Column("comment_id", sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column("post_id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("content", sa.String(500), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["post_id"], ["community_posts.post_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("comment_id"),
    )

    op.create_table(
        "report",
        sa.Column("report_id", sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("report_type", sa.String(20), nullable=False),
        sa.Column("target_type", sa.String(20), nullable=True),
        sa.Column("target_id", sa.BigInteger(), nullable=False),
        sa.Column("report_reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("status", sa.String(20), nullable=False, server_default="PENDING"),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("report_id"),
        sa.CheckConstraint(
            "report_type IN ('ILLEGAL', 'SPAM', 'ABUSE', 'PLAGIARISM', 'OTHER')",
            name="ck_report_type",
        ),
        sa.CheckConstraint(
            "target_type IN ('SERVICE', 'COMMUNITY', 'FEEDBACK', 'COMMENT')",
            name="ck_report_target_type",
        ),
        sa.CheckConstraint("status IN ('PENDING', 'APPROVED', 'REJECTED')", name="ck_report_status"),
    )

    op.create_table(
        "service_entry_logs",
        sa.Column("log_id", sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=True),
        sa.Column("session_id", sa.String(255), nullable=True),
        sa.Column("service_id", sa.BigInteger(), nullable=False),
        sa.Column("promo_product_id", sa.Integer(), nullable=True),
        sa.Column("occurred_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("source_page", sa.String(100), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
        sa.ForeignKeyConstraint(["service_id"], ["services.service_id"]),
        sa.ForeignKeyConstraint(["promo_product_id"], ["promotion_products.promo_product_id"]),
        sa.PrimaryKeyConstraint("log_id"),
    )

    op.create_table(
        "user_follows",
        sa.Column("follow_id", sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column("follower_id", sa.BigInteger(), nullable=False),
        sa.Column("following_id", sa.BigInteger(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(), nullable=True, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["follower_id"], ["users.user_id"]),
        sa.ForeignKeyConstraint(["following_id"], ["users.user_id"]),
        sa.PrimaryKeyConstraint("follow_id"),
        sa.UniqueConstraint("follower_id", "following_id", name="uq_user_follows"),
    )


def downgrade() -> None:
    op.drop_table("user_follows")
    op.drop_table("service_entry_logs")
    op.drop_table("report")
    op.drop_table("community_comments")
    op.drop_table("community_posts")
    op.drop_table("point_logs")
    op.drop_table("promotions")
    op.drop_table("promotion_products")
    op.drop_table("feedbacks")
    op.drop_table("services")
    op.drop_table("attendance")
    op.drop_table("user_interests")
    op.drop_table("users")
    op.drop_table("categories")
