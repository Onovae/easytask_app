# 🚀 EasyTask Deployment Guide

Complete guide to deploy EasyTask (Frontend + Backend) to production.

## 📋 Table of Contents
1. [Frontend Deployment (Vercel)](#frontend-deployment-vercel---free)
2. [Backend Deployment Options](#backend-deployment-options)
3. [Post-Deployment Setup](#post-deployment-setup)

---

## Frontend Deployment (Vercel - FREE)

### Prerequisites
- ✅ Node.js installed
- ✅ GitHub account
- ✅ Vercel account (sign up at https://vercel.com)

### Step 1: Install Node.js (if not installed)

1. Download from https://nodejs.org/ (LTS version recommended)
2. Install and verify:
   ```powershell
   node --version
   npm --version
   ```

### Step 2: Test Locally

```powershell
cd frontend/client
npm install
npm run dev
```

Visit http://localhost:3000 and test:
- ✅ Registration with email OTP
- ✅ Login
- ✅ Create tasks
- ✅ Mark tasks as done
- ✅ Delete tasks

### Step 3: Push to GitHub

```powershell
# In your project root
git add .
git commit -m "Add React frontend"
git push
```

### Step 4: Deploy to Vercel

#### Method 1: Vercel Dashboard (Recommended)

1. **Go to https://vercel.com** and sign in
2. Click **"New Project"**
3. **Import your GitHub repository**
4. **Configure:**
   - Framework Preset: **Vite**
   - Root Directory: **frontend/client**
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. **Add Environment Variable:**
   - Key: `VITE_API_URL`
   - Value: Your backend URL (e.g., `https://your-backend.com`)
6. Click **"Deploy"**
7. **Done!** 🎉 Your app will be live in ~1 minute

#### Method 2: Vercel CLI

```powershell
npm i -g vercel
vercel login
cd frontend/client
vercel
```

Follow the prompts and your app will be deployed!

### Step 5: Update Backend CORS

After deployment, update your backend `.env` to allow your Vercel URL:

```env
# In backend .env
FRONTEND_URL=https://your-app.vercel.app
```

Restart your backend server.

---

## Backend Deployment Options

You have several FREE options for hosting your FastAPI backend:

### Option 1: Render.com (Recommended - FREE)

**Pros:** Free tier, auto-deploys from GitHub, built-in PostgreSQL
**Cons:** Free tier sleeps after inactivity (wakes up in ~30 seconds)

1. **Create account** at https://render.com
2. **New Web Service** → Connect GitHub repo
3. **Configure:**
   - Name: `easytask-api`
   - Root Directory: `.` (project root)
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Add Environment Variables:**
   ```
   DATABASE_URL=postgresql://...
   RESEND_API_KEY=re_...
   EMAIL_FROM=EasyTask <noreply@maureenonovae.cv>
   FRONTEND_URL=https://your-app.vercel.app
   SECRET_KEY=your-secret-key
   ```
5. **Create PostgreSQL Database:**
   - In Render dashboard: New → PostgreSQL
   - Copy **Internal Database URL**
   - Add to `DATABASE_URL` environment variable
6. **Deploy!**

### Option 2: Railway.app (FREE)

**Pros:** Very easy, free tier, good performance
**Cons:** $5 credit per month (usually enough for free usage)

1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Add PostgreSQL service
4. Add environment variables
5. Deploy!

### Option 3: Fly.io (FREE)

**Pros:** Always-on (doesn't sleep), good free tier
**Cons:** Requires Docker knowledge

1. Install Fly CLI
2. Run `fly launch`
3. Follow prompts
4. Deploy!

---

## Post-Deployment Setup

### 1. Update Frontend Environment

After backend is deployed, update Vercel environment variable:

1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Update `VITE_API_URL` to your backend URL
3. Redeploy (Vercel will auto-redeploy)

### 2. Run Database Migrations

SSH into your backend server or use their CLI:

```bash
alembic upgrade head
```

### 3. Test Production

1. Visit your Vercel URL
2. Register a new user
3. Check email for OTP
4. Verify email
5. Login and create tasks
6. Success! 🎉

### 4. Custom Domain (Optional)

#### For Frontend (Vercel):
1. Vercel Dashboard → Your Project → Settings → Domains
2. Add `341339742641803264.hello.cv` or `maureenonovae.cv`
3. Follow DNS instructions

#### For Backend (Render/Railway/Fly):
1. Similar process in their dashboard
2. Add custom domain
3. Update SSL certificates

---

## 🔍 Troubleshooting

### Frontend Issues

**"Failed to fetch" errors:**
- Check `VITE_API_URL` is correct in Vercel
- Verify backend CORS allows your Vercel URL
- Check backend is running

**OTP emails not sending:**
- Verify `RESEND_API_KEY` in backend
- Check domain is verified (maureenonovae.cv)
- Look at backend logs

### Backend Issues

**Database connection errors:**
- Verify `DATABASE_URL` is correct
- Run migrations: `alembic upgrade head`
- Check PostgreSQL is running

**CORS errors:**
- Add Vercel URL to `FRONTEND_URL` in backend `.env`
- Restart backend after changes

---

## 📊 Cost Summary

| Service | Free Tier | Paid |
|---------|-----------|------|
| **Vercel** (Frontend) | Unlimited sites | $20/month for pro features |
| **Render** (Backend) | 750 hours/month | $7/month for always-on |
| **Railway** (Backend) | $5 credit/month | Pay as you go |
| **Fly.io** (Backend) | 3 VMs free | Pay as you go |
| **Resend** (Email) | 3,000 emails/month | $20/month for more |

**Total for FREE tier:** $0/month! 🎉

---

## 🎯 Recommended Setup

For production with zero cost:

1. ✅ **Frontend:** Vercel (free, fast, auto-deploys)
2. ✅ **Backend:** Render.com (free tier with PostgreSQL)
3. ✅ **Email:** Resend (3,000 free emails/month)
4. ✅ **Domain:** maureenonovae.cv (already have it!)

This gives you a fully functional, production-ready app at **zero cost**!

---

## 📝 Next Steps

After deployment:
1. ✅ Test all features in production
2. ✅ Monitor error logs
3. ✅ Set up analytics (optional)
4. ✅ Add more features!

Need help? Check the logs in each platform's dashboard.
