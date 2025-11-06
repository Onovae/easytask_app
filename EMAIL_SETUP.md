# 📧 Email Setup Guide for EasyTask

## Email Verification System

EasyTask now supports **TWO** verification methods:

### 1. 🔢 Email OTP (Current - No Frontend Needed!)
- User registers → Receives 6-digit code via email → Enters code to verify
- **Works NOW** without frontend
- Perfect for testing and API-only usage

### 2. 🔗 Email Link (For Future Frontend)
- User registers → Receives verification link → Clicks to verify
- **Requires frontend** (will work when you deploy to GitHub Pages)
- Better user experience for web apps

Both methods work simultaneously! You can use OTP now and switch to link verification when your frontend is ready.

---

## Using Resend (Recommended - FREE & Easy!)

Resend is the simplest email service to set up and works perfectly with your GitHub Pages frontend.

### Step 1: Sign up for Resend

1. Go to https://resend.com/
2. Click "Start Building" or "Sign Up"
3. Sign up with your email or GitHub account
4. **It's FREE** - 3,000 emails/month, no credit card required!

### Step 2: Get your API Key

1. After logging in, go to **API Keys** in the dashboard
2. Click "Create API Key"
3. Give it a name (e.g., "EasyTask Production")
4. Copy the API key (starts with `re_...`)

### Step 3: Add to your .env file

Open your `.env` file and add:

```bash
RESEND_API_KEY=re_your_actual_api_key_here
EMAIL_FROM=EasyTask <onboarding@resend.dev>
```

**Important:** For testing, you can use `onboarding@resend.dev` as the sender. 
For production, you'll need to verify your own domain (also free).

### Step 4: Restart your server

The server should auto-reload, but if not:
- Press `Ctrl+C` in the terminal
- Run: `uvicorn app.main:app --reload`

### Step 5: Test it!

Try registering a user in the API docs (http://127.0.0.1:8000/docs)

#### Testing Email OTP Flow:
1. Go to **POST /api/auth/register**
2. Register with: `maureenonovae@gmail.com` (or any email if domain is verified)
3. Check your email for the 6-digit OTP code
4. Use **POST /api/auth/verify-email-otp** with your email and the OTP code
5. Done! User is verified ✅

#### If Email Doesn't Send:
- The OTP will be included in the registration response for testing
- Just copy it and use it with `/verify-email-otp`

**⚠️ IMPORTANT FOR TESTING:**
- In test mode, Resend only sends emails to **your verified email** (maureenonovae@gmail.com)
- To test, register with: `maureenonovae@gmail.com`
- To send to other emails, you need to verify a domain (see below)

---

## Verify Your Own Domain (Required for Production)

To send from your own domain (e.g., `noreply@yourdomain.com`):

1. In Resend dashboard, go to **Domains**
2. Click "Add Domain"
3. Enter your domain name
4. Add the DNS records Resend provides to your domain's DNS settings
5. Wait for verification (usually 5-10 minutes)
6. Update `.env`:
   ```bash
   EMAIL_FROM=EasyTask <noreply@yourdomain.com>
   ```

---

## Alternative: Using Brevo

If you prefer Brevo, keep the existing Brevo settings in your `.env` and the app will use that instead.

---

## Testing Email Delivery

### Method 1: Email OTP (Current)
1. Register a new user with your email
2. Check your email for the 6-digit code
3. Call `/verify-email-otp` with your email and code
4. You're verified! 🎉

### Method 2: Email Link (When Frontend is Ready)
1. Register a new user with your email
2. Check your inbox (and spam folder)
3. Click the verification link
4. You're done! 🎉

---

## Available Endpoints

### Email OTP Verification (Works Now!)
- `POST /api/auth/register` - Register user, sends OTP to email
- `POST /api/auth/verify-email-otp` - Verify with email + OTP code
- `POST /api/auth/resend-email-otp` - Resend OTP if expired

### Email Link Verification (For Frontend)
- `GET /api/auth/verify-email?token=xxx` - Verify via link (requires frontend)

### SMS OTP Verification (Already Working!)
- `POST /api/auth/send-otp` - Send OTP to phone
- `POST /api/auth/verify-otp` - Verify with phone OTP

---

## Troubleshooting

**Emails not sending?**
- Check that `RESEND_API_KEY` is set in `.env`
- Make sure the API key is correct (no extra spaces)
- Check the server logs for error messages
- Verify the email address is valid

**Emails going to spam?**
- For testing with `onboarding@resend.dev`, this is normal
- For production, verify your own domain
- Add SPF and DKIM records (Resend provides these)
