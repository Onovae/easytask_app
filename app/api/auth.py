from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.schemas.user import (
    UserCreate, UserRead, UserLogin, UserOut, UserUpdate, UserProfile, ChangePasswordRequest
)
from app.models.user import User
from app.crud import user as crud_user
from app.core.security import (
    verify_password, create_access_token, create_email_token,
    verify_email_token, get_current_user, hash_password
)
from app.db.session import get_db
from app.utils.emails import send_email
from app.utils.sms import generate_otp, send_otp_sms
from app.core.config import get_settings
from app.models.otp_entry import OtpEntry
from datetime import datetime, timedelta
from datetime import timezone

settings = get_settings()
router = APIRouter()


@router.post("/register", status_code=201)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        password_hash=hash_password(user_in.password),
        phone_number=user_in.phone_number
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_email_token(user_in.email)
    verify_url = f"{settings.app.FRONTEND_URL}/verify-email?token={token}"
    send_email(
        to_email=user_in.email,
        subject="Verify Your Email",
        body=f"<p>Click <a href='{verify_url}'>here</a> to verify your email.</p>"
    )

    return {"msg": "Verify your email address before logging in."}



@router.post("/send-otp")
def send_otp(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user is None or user.phone_number is None:
        raise HTTPException(404, "User or phone not found")

    otp = generate_otp()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
    db.query(OtpEntry).filter(OtpEntry.phone == user.phone_number).delete()
    db.add(OtpEntry(phone=user.phone_number, code=otp, expires_at=expires_at))
    db.commit()

    phone_number = getattr(user, "phone_number", None)
    if not isinstance(phone_number, str) or not phone_number:
        raise HTTPException(status_code=400, detail="Invalid phone number")
    send_otp_sms(phone_number, otp)
    return {"msg": "OTP sent"}


@router.post("/verify-otp")
def verify_otp(email: str, otp: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user or not user.phone_number:
            raise HTTPException(status_code=404, detail="User or phone number not found")

        otp_entry = db.query(OtpEntry).filter(OtpEntry.phone == user.phone_number).first()
        if not otp_entry:
            raise HTTPException(status_code=404, detail="OTP not found")

        if otp_entry.code != otp:
            raise HTTPException(status_code=401, detail="Invalid OTP")

        if otp_entry.expires_at is not None and otp_entry.expires_at < datetime.utcnow():
            raise HTTPException(status_code=401, detail="OTP expired")

        user.is_verified = True
        db.delete(otp_entry)
        db.commit()

        return {"msg": "OTP verified and user marked as verified"}

    except HTTPException:
        raise  # Re-raise expected HTTP errors
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server error during OTP verification: {str(e)}")


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, getattr(user, "password_hash", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/user/profile", response_model=UserOut)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/password-reset-request")
def request_password_reset(email: EmailStr, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_email_token(str(user.email))
    reset_link = f"{settings.app.FRONTEND_URL}/reset-password?token={token}"
    
    send_email(
        to_email=str(user.email),
        subject="Reset Your Password",
        body=f"<p>Click <a href='{reset_link}'>here</a> to reset your password.</p>"
    )

    return {"msg": "Password reset email sent"}

@router.post("/reset-password")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    email = verify_email_token(token)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    setattr(user, "password_hash", hash_password(new_password))
    db.commit()
    return {"msg": "Password reset successful"}


