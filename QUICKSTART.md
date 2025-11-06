# 🚀 Quick Start Guide - EasyTask Frontend

## Prerequisites Check

❌ **Node.js NOT installed** - You need to install this first!

---

## Step 1: Install Node.js

### Download & Install:

1. **Go to:** https://nodejs.org/
2. **Download:** Click the **LTS version** (Long Term Support) - currently v20.x or v22.x
   - This is the green button on the left
   - LTS = Most stable version
3. **Run the installer:**
   - Accept all defaults
   - Click "Next" through the installation
   - It will install both Node.js and npm (package manager)
4. **Verify installation:**
   - Close ALL PowerShell windows
   - Open a NEW PowerShell window
   - Run these commands:
   ```powershell
   node --version
   # Should show: v20.x.x or similar
   
   npm --version
   # Should show: 10.x.x or similar
   ```

---

## Step 2: Install Frontend Dependencies

After Node.js is installed:

```powershell
# Navigate to frontend directory
cd C:\Users\PERI\Desktop\Maureen_dev\easytask_app\frontend\client

# Install all dependencies
npm install
```

This will install:
- ✅ React 18
- ✅ Vite (build tool)
- ✅ Tailwind CSS
- ✅ React Router
- ✅ Axios (for API calls)

---

## Step 3: Start Development Server

```powershell
npm run dev
```

You should see:
```
  VITE v5.4.5  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

---

## Step 4: Open in Browser

Open your browser and go to: **http://localhost:3000**

You should see the **EasyTask login page**! 🎉

---

## Step 5: Test the App

### Test Registration Flow:

1. **Click "Sign up"** on the login page
2. **Fill in the form:**
   - Full Name: Your name
   - Email: `maureenonovae@gmail.com` (or any email - domain is verified!)
   - Phone: Optional
   - Password: At least 6 characters
3. **Click "Create account"**
4. **Check your email** for the 6-digit OTP code
5. **Enter the OTP** on the verification page
6. **Success!** You'll be redirected to login

### Test Login & Tasks:

1. **Login** with your email and password
2. **Click "+ New Task"**
3. **Create a task** with title and description
4. **Check it off** when done
5. **Delete it** if needed

---

## Troubleshooting

### "npm: The term 'npm' is not recognized"
- ❌ Node.js is not installed OR
- ❌ You didn't close and reopen PowerShell after installation
- ✅ **Solution:** Install Node.js from https://nodejs.org/, then close ALL PowerShell windows and open a new one

### "Cannot find module 'react'"
- ❌ Dependencies not installed
- ✅ **Solution:** Run `npm install` in the `frontend/client` directory

### "Port 3000 already in use"
- ❌ Another app is using port 3000
- ✅ **Solution:** 
  ```powershell
  # Use a different port
  npm run dev -- --port 3001
  ```

### Backend connection errors
- ❌ Backend is not running
- ✅ **Solution:** Start the backend in a separate PowerShell window:
  ```powershell
  cd C:\Users\PERI\Desktop\Maureen_dev\easytask_app
  .\venv\Scripts\Activate.ps1
  uvicorn app.main:app --reload
  ```

---

## Next Steps After Testing

Once everything works locally:

1. ✅ **Push to GitHub:**
   ```powershell
   git add .
   git commit -m "Add React frontend"
   git push
   ```

2. ✅ **Deploy to Vercel:**
   - Go to https://vercel.com
   - Click "New Project"
   - Import your GitHub repo
   - Root Directory: `frontend/client`
   - Environment Variable: `VITE_API_URL` = your backend URL
   - Click "Deploy"

3. ✅ **Celebrate!** 🎉 You have a fully functional app!

---

## Summary

**Before you can run the frontend:**
1. Install Node.js from https://nodejs.org/ (LTS version)
2. Close and reopen PowerShell
3. Run `npm install` in `frontend/client` directory
4. Run `npm run dev`
5. Open http://localhost:3000

**That's it!** The frontend is already built and ready to go - you just need Node.js to run it.
