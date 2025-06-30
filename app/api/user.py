from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserProfile, UserUpdate, UserOut, ChangePasswordRequest
from app.db.session import get_db
from app.models.user import User
from app.core.security import get_current_user, verify_password, hash_password

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/profile", response_model=UserOut)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/profile", response_model=UserOut)
def update_profile(
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if payload.full_name is not None:
        setattr(current_user, "full_name", payload.full_name)
    if payload.email is not None:
        setattr(current_user, "email", str(payload.email))
    if hasattr(payload, "phone_number") and payload.phone_number is not None:
        setattr(current_user, "phone_number", payload.phone_number)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.put("/change-password")
def change_password(
    req: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(req.current_password, getattr(current_user, "password_hash")):
        raise HTTPException(status_code=403, detail="Current password is incorrect")
    setattr(current_user, "password_hash", hash_password(req.new_password))
    db.commit()
    return {"msg": "Password updated successfully"}