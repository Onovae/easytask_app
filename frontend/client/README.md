# EasyTask Frontend

Modern, clean React frontend for EasyTask - built with Vite, React Router, and Tailwind CSS.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ installed ([Download here](https://nodejs.org/))

### Installation

1. **Install dependencies:**
   ```powershell
   cd frontend/client
   npm install
   ```

2. **Start development server:**
   ```powershell
   npm run dev
   ```

3. **Open in browser:**
   Visit http://localhost:3000

## 🌟 Features

- ✅ **User Registration** with email OTP verification
- ✅ **Login/Logout** with JWT authentication
- ✅ **Task Management** (Create, Read, Update, Delete)
- ✅ **Email Verification** via 6-digit OTP code
- ✅ **Responsive Design** - works on all devices
- ✅ **Modern UI** with Tailwind CSS

## 📁 Project Structure

```
src/
├── components/       # Reusable components
│   └── Layout.jsx   # Main layout with navigation
├── context/         # React context for state management
│   └── AuthContext.jsx  # Authentication context
├── pages/           # Page components
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── VerifyEmail.jsx
│   └── Dashboard.jsx
├── App.jsx          # Main app with routing
├── main.jsx         # Entry point
└── index.css        # Global styles with Tailwind
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the `frontend/client` directory:

```env
VITE_API_URL=http://127.0.0.1:8000
```

For production, update this to your deployed backend URL.

## 📦 Build for Production

```powershell
npm run build
```

The optimized build will be in the `dist/` folder.

## 🚀 Deploy to Vercel (Recommended - FREE)

### Option 1: Via Vercel Dashboard (Easiest)

1. **Push to GitHub:**
   ```powershell
   git add .
   git commit -m "Add frontend"
   git push
   ```

2. **Deploy to Vercel:**
   - Go to https://vercel.com
   - Click "New Project"
   - Import your GitHub repository
   - Set **Root Directory** to: `frontend/client`
   - Add environment variable: `VITE_API_URL` = your backend URL
   - Click "Deploy"

3. **Done!** Your app will be live in seconds 🎉

### Option 2: Via Vercel CLI

```powershell
npm i -g vercel
vercel login
vercel
```

## 🎨 Customization

### Change Colors
Edit `tailwind.config.js` to customize the color scheme:

```js
colors: {
  primary: {
    // Change these values
    500: '#0ea5e9',  // Main color
    600: '#0284c7',  // Darker shade
    // ...
  }
}
```

### Add More Pages
1. Create new component in `src/pages/`
2. Add route in `src/App.jsx`
3. Add navigation link in `src/components/Layout.jsx`

## 🔍 API Integration

The frontend connects to your FastAPI backend at the URL specified in `VITE_API_URL`.

### Endpoints Used:
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/verify-email-otp` - Email verification
- `POST /api/auth/resend-email-otp` - Resend OTP
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create task
- `PATCH /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

## 🆘 Troubleshooting

**"npm: The term 'npm' is not recognized"**
- Install Node.js from https://nodejs.org/

**CORS errors in browser console**
- Make sure your backend CORS settings allow your frontend URL
- Backend should allow `http://localhost:3000` for local development

**"Failed to fetch" errors**
- Check that backend is running at the URL in `.env`
- Verify `VITE_API_URL` is correct

## 📝 License

MIT
