"""
categories와 promotion_products 기준 데이터를 삽입한다.
이미 데이터가 있으면 건너뛴다.
"""
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.promotion import PromotionProduct


CATEGORIES = [
    "IT/개발",
    "디자인",
    "마케팅",
    "교육",
    "헬스/뷰티",
    "푸드",
    "여행",
    "금융",
    "엔터테인먼트",
    "기타",
]

PROMOTION_PRODUCTS = [
    {
        "promo_product_name": "홈 배너 1일",
        "price": 500,
        "duration_days": 1,
        "placement": "home_banner",
        "slot_limit": 3,
        "is_active": True,
    },
    {
        "promo_product_name": "홈 팝업 1일",
        "price": 800,
        "duration_days": 1,
        "placement": "home_popup",
        "slot_limit": 1,
        "is_active": True,
    },
    {
        "promo_product_name": "서비스 목록 상단 1일",
        "price": 300,
        "duration_days": 1,
        "placement": "service_list_top",
        "slot_limit": 5,
        "is_active": True,
    },
    {
        "promo_product_name": "홈 배너 3일",
        "price": 1400,
        "duration_days": 3,
        "placement": "home_banner",
        "slot_limit": 3,
        "is_active": False,
    },
    {
        "promo_product_name": "홈 배너 7일",
        "price": 3000,
        "duration_days": 7,
        "placement": "home_banner",
        "slot_limit": 3,
        "is_active": False,
    },
]


def seed_categories(db: Session) -> None:
    if db.query(Category).count() > 0:
        return
    for name in CATEGORIES:
        db.add(Category(category_name=name))
    db.commit()


def seed_promotion_products(db: Session) -> None:
    if db.query(PromotionProduct).count() > 0:
        return
    for data in PROMOTION_PRODUCTS:
        db.add(PromotionProduct(**data))
    db.commit()


def run_seed(db: Session) -> None:
    seed_categories(db)
    seed_promotion_products(db)
