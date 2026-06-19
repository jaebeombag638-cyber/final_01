from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db.session import make_session


def get_db() -> Generator[Session, None, None]:
    db = make_session()
    try:
        yield db
    finally:
        db.close()
