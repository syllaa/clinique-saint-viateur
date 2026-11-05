from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.user import User

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def _create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + expires_delta
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_access_token(user: User) -> str:
    return _create_token(
        {"sub": user.username, "role": user.role, "type": "access"},
        timedelta(minutes=settings.access_token_expire_minutes),
    )


def create_refresh_token(user: User) -> str:
    return _create_token(
        {"sub": user.username, "type": "refresh"},
        timedelta(days=settings.refresh_token_expire_days),
    )


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        return None


# Passwords refused outright, whatever their length (includes the seed default).
_COMMON_PASSWORDS = {
    "admin123", "password", "motdepasse", "azerty123", "qwerty123", "123456789",
    "1234567890", "administrateur", "clinique123", "saintviateur",
}


def password_problem(new_password: str, username: str) -> str | None:
    """Returns a French message describing why the password is too weak, or None."""
    if len(new_password) < 10:
        return "Le mot de passe doit contenir au moins 10 caractères."
    if not any(c.isalpha() for c in new_password) or not any(c.isdigit() for c in new_password):
        return "Le mot de passe doit contenir au moins une lettre et un chiffre."
    lowered = new_password.lower()
    if lowered in _COMMON_PASSWORDS or lowered == username.lower():
        return "Ce mot de passe est trop courant. Choisissez-en un autre."
    return None


def change_password(db: Session, user: User, new_password: str) -> None:
    user.hashed_password = hash_password(new_password)
    db.commit()


def uses_default_password(db: Session) -> bool:
    """True if the seed admin account still has the documented default password."""
    user = get_user_by_username(db, settings.admin_username)
    return bool(user and verify_password("admin123", user.hashed_password))


def ensure_seed_admin(db: Session) -> None:
    """Create the initial admin user from settings if the users table is empty."""
    if db.query(User).first() is not None:
        return
    admin = User(
        username=settings.admin_username,
        hashed_password=hash_password(settings.admin_password),
        role="admin",
    )
    db.add(admin)
    db.commit()
