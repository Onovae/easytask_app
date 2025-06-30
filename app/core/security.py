from datetime import datetime, timedelta, timezone
from typing import Optional

from uuid import UUID  
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.db.session import get_db
from app.models.user import User
from app.core.config import get_settings

# Load settings and password context
settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
# Password hashing and verification functions
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(
        minutes=settings.app.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.app.SECRET_KEY, algorithm="HS256")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.app.SECRET_KEY, algorithms=["HS256"])
        user_id: Optional[str] = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_uuid = UUID(user_id)  # Convert safely to UUID
    except (JWTError, ValueError):
        raise credentials_exception

    user = db.query(User).filter(User.id == user_uuid).first()
    if user is None:
        raise credentials_exception
    return user



def create_email_token(email: str, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(hours=1))
    token = {"sub": email, "exp": expire}
    return jwt.encode(token, settings.app.SECRET_KEY, algorithm="HS256")

def verify_email_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.app.SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token payload")
        return email
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

