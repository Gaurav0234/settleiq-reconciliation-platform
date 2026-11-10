
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User


def get_user_by_email(db: Session, email: str) -> User | None:
    normalized_email = email.strip().lower()

    return db.scalar(
        select(User).where(User.email == normalized_email)
    )


def register_user(
    db: Session,
    full_name: str,
    email: str,
    password: str,
) -> User:
    normalized_email = email.strip().lower()

    existing_user = get_user_by_email(db, normalized_email)

    if existing_user:
        raise ValueError("An account with this email already exists")

    user = User(
        full_name=full_name.strip(),
        email=normalized_email,
        hashed_password=hash_password(password),
        role="finance_executive",
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    if not user.is_active:
        return None

    return user
