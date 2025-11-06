from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.schemas.user import (
    UserCreate, UserRead, UserLogin, UserOut, UserUpdate, UserProfile, 
    ChangePasswordRequest, VerifyEmailOTP, ResendEmailOTP
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

    # Generate OTP for email verification
    otp = generate_otp()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
    
    # Store OTP in database
    db.query(OtpEntry).filter(OtpEntry.email == user_in.email).delete()
    db.add(OtpEntry(email=user_in.email, code=otp, expires_at=expires_at))
    db.commit()

    # Try to send OTP email
    try:
        send_email(
            to_email=user_in.email,
            subject="Verify Your EasyTask Account",
            body=f"""
            <h2>Welcome to EasyTask!</h2>
            <p>Your verification code is:</p>
            <h1 style="color: #4CAF50; font-size: 32px; letter-spacing: 5px;">{otp}</h1>
            <p>This code will expire in 10 minutes.</p>
            <p>If you didn't create an account, please ignore this email.</p>
            """
        )
        return {
            "msg": "User registered successfully. Please check your email for the verification code.",
            "note": "Use the /verify-email-otp endpoint to verify your account with the code."
        }
    except Exception as e:
        error_msg = str(e)
        print(f"Warning: Could not send OTP email: {e}")
        
        # Check if it's a Resend domain verification issue
        if "verify a domain" in error_msg.lower():
            return {
                "msg": "User registered successfully.",
                "otp": otp,  # Return OTP in response for testing
                "note": "Email delivery requires a verified domain. For testing, the OTP is included in this response. Use /verify-email-otp to verify."
            }
        
        return {
            "msg": "User registered successfully.",
            "otp": otp,  # Return OTP in response as fallback
            "note": "Email delivery is currently unavailable. Use the OTP above with /verify-email-otp to verify."
        }



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

            # Compare expiry safely (handle naive vs aware datetimes)
            now_utc = datetime.now(timezone.utc)
            exp = otp_entry.expires_at
            if exp is not None:
                if exp.tzinfo is None:
                    exp = exp.replace(tzinfo=timezone.utc)
                if exp < now_utc:
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


@router.post("/verify-email-otp")
def verify_email_otp(data: VerifyEmailOTP, db: Session = Depends(get_db)):
    """Verify email using OTP code sent to email"""
    try:
        user = db.query(User).filter(User.email == data.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check OTP
        otp_entry = db.query(OtpEntry).filter(OtpEntry.email == data.email).first()
        if not otp_entry:
            raise HTTPException(status_code=404, detail="OTP not found. Please request a new one.")
        
        # Debug logging
        print(f"DEBUG: Received OTP: '{data.otp}', Stored OTP: '{otp_entry.code}'")
        print(f"DEBUG: OTP types - Received: {type(data.otp)}, Stored: {type(otp_entry.code)}")
        
        if otp_entry.code != data.otp:
            raise HTTPException(status_code=401, detail=f"Invalid OTP. Received: {data.otp}, Expected: {otp_entry.code}")
        
            # Compare expiry safely (handle naive vs aware datetimes)
            now_utc = datetime.now(timezone.utc)
            exp = otp_entry.expires_at
            if exp is not None:
                if exp.tzinfo is None:
                    exp = exp.replace(tzinfo=timezone.utc)
                if exp < now_utc:
                    raise HTTPException(status_code=401, detail="OTP expired. Please request a new one.")
        
        # Mark user as verified and delete OTP
        user.is_verified = True
        db.delete(otp_entry)
        db.commit()
        
        return {"msg": "Email verified successfully! You can now login."}
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/resend-email-otp")
def resend_email_otp(data: ResendEmailOTP, db: Session = Depends(get_db)):
    """Resend OTP to email"""
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.is_verified:
        raise HTTPException(status_code=400, detail="Email already verified")
    
    # Generate new OTP
    otp = generate_otp()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
    
    # Update or create OTP entry
    db.query(OtpEntry).filter(OtpEntry.email == data.email).delete()
    db.add(OtpEntry(email=data.email, code=otp, expires_at=expires_at))
    db.commit()
    
    # Send OTP email
    try:
        send_email(
            to_email=data.email,
            subject="Your New EasyTask Verification Code",
            body=f"""
            <h2>EasyTask Verification</h2>
            <p>Your new verification code is:</p>
            <h1 style="color: #4CAF50; font-size: 32px; letter-spacing: 5px;">{otp}</h1>
            <p>This code will expire in 10 minutes.</p>
            """
        )
        return {"msg": "New verification code sent to your email."}
    except Exception as e:
        print(f"Warning: Could not send OTP email: {e}")
        return {
            "msg": "New verification code generated.",
            "otp": otp,
            "note": "Email delivery failed. Use the OTP above to verify."
        }


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    """Verify email using the token from the verification link (for frontend use)"""
    try:
        email = verify_email_token(token)
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.is_verified = True
        db.commit()
        
        return {"msg": "Email verified successfully! You can now login."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, getattr(user, "password_hash", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Check if user is verified
    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please verify your email before logging in")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "is_verified": user.is_verified
        }
    }

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
    
    try:
        send_email(
            to_email=str(user.email),
            subject="Reset Your Password",
            body=f"<p>Click <a href='{reset_link}'>here</a> to reset your password.</p>"
        )
        return {"msg": "Password reset email sent"}
    except Exception as e:
        print(f"Warning: Could not send password reset email: {e}")
        return {"msg": "Password reset email service is currently unavailable", "token": token}

@router.post("/reset-password")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    email = verify_email_token(token)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    setattr(user, "password_hash", hash_password(new_password))
    db.commit()
    return {"msg": "Password reset successful"}


