# 📝 EasyTask – Smart Task Manager with OTP & Email Verification

**EasyTask** is a lightweight task management app built with a robust FastAPI backend and a clean React frontend. It helps users organize their to-dos while incorporating secure user registration, email verification, and OTP-based phone authentication.

---

## 🚀 Features

- ✅ **User Registration & Login**  
  Secure signup with email, password hashing, and JWT login tokens.

- 📧 **Email Verification**  
  Verification links are sent via email using Brevo (SMTP) to activate accounts.

- 📱 **OTP Phone Authentication**  
  One-time password (OTP) sent via Twilio to verify users' phone numbers.

- 🧠 **Task Management**  
  Create, update, mark complete, and delete tasks with reminder support.

- 🛡️ **Password Reset**  
  Forgot password? Request a reset link and set a new one via email.

- 🌐 **Fully RESTful API**  
  Built using FastAPI, SQLAlchemy, and Alembic for clean migrations.

- 💻 **Frontend**  
  Simple React SPA deployed on GitHub Pages for intuitive interaction.

---

## 🛠️ Technologies Used

**Backend**
- Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Alembic (migrations)
- Twilio (OTP SMS)
- Brevo (Email via SMTP)

**Frontend**
- React (via Create React App)
- GitHub Pages (for deployment)

**DevOps**
- Docker-ready
- Git & GitHub for version control

---

## 🧪 Local Development Setup

```bash
# Backend
cd easytask_app
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm start


⚙️ Environment Variables
Create a .env file in the root of the backend with:

SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
POSTGRES_USER=your_pg_user
POSTGRES_PASSWORD=your_pg_pass
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=easytask_db
SMTP_HOST=smtp-relay.brevo.com
SMTP_USER=your_email
SMTP_PASSWORD=your_email_password
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890
FRONTEND_URL=http://localhost:3000


🔐 Security
Passwords are hashed using passlib.

JWT tokens are used for login and protected routes.

Emails and OTPs are verified before user access is granted.

🧠 Future Enhancements
Add Task labels and priorities

Enable Google login with OAuth2

Build mobile version with React Native

Push notifications for task reminders


👨‍💻 Author
Onovae Maureen
Built as a requirement for the daily learning on building a Full Stack Web Application
GitHub: @Onovae

🌍 Live Demo
🔗 View Frontend on GitHub Pages

🔗 API Base URL (Local)

📄 License
This project is open source and available under the MIT License.