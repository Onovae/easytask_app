from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()



def get_user_profile(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def update_user_profile(db: Session, user: User, updates: UserUpdate) -> User:
    if updates.email:
        user.email = updates.email
    if updates.full_name:
        user.full_name = updates.full_name
    db.commit()
    db.refresh(user)
    return user

def get_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_in: UserCreate):
    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=hash_password(user_in.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user: User, user_in: UserUpdate):
    if user_in.name:
        user.full_name = user_in.name
    if user_in.email:
        user.email = user_in.email
    db.commit()
    db.refresh(user)
    return user
