from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth
from app.api import user
from app.api import task
from app.db.base import Base
from app.db.session import engine
from app.utils.reminder import start_reminder_thread

app = FastAPI(title="EasyTask App", version="1.0.0")

# Create tables (not for production use — use Alembic later!)
Base.metadata.create_all(bind=engine)

# CORS (we will restrict origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(task.router, prefix="/api/tasks", tags=["Tasks"])


# # Start reminder thread
start_reminder_thread()

