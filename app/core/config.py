# config.py
from typing import List, Optional
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

# ─────────────── App Settings ───────────────
class AppSettings(BaseSettings):
    APP_NAME: str = "EasyTask"
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "IZzFyc4an-m8Vtw-p60j2lxpyF7eWT6Krk29l-XB_gI"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CORS_ORIGINS: List[AnyHttpUrl] = []
    FRONTEND_URL: str = "http://localhost:3000"
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# ─────────────── DB Settings ───────────────
class DatabaseSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# ─────────────── Email Settings ───────────────
class EmailSettings(BaseSettings):
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""
    SMTP_TLS: bool = True
    BREVO_API_KEY: str = ""
    SMS_SENDER: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# ─────────────── AI Settings ───────────────
class AISettings(BaseSettings):
    OPENAI_API_KEY: Optional[str] = None
    HF_API_KEY: Optional[str] = None
    ENABLE_AI_FEATURES: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# ─────────────── Unified Access ───────────────
class Settings:
    app = AppSettings()
    db = DatabaseSettings()
    email = EmailSettings()
    ai = AISettings()

    @property
    def SECRET_KEY(self):
        return self.app.SECRET_KEY

    @property
    def FRONTEND_URL(self):
        return self.app.FRONTEND_URL

    class Config:
        env_file = ".env"



@lru_cache()
def get_settings() -> Settings:
    return Settings()

