# 🔧 Browser Testing Guide

## ✅ Backend Status: WORKING PERFECTLY

- Login endpoint: ✓
- Token generation: ✓
- /auth/me endpoint: ✓
- /routers/ endpoint: ✓

## 🌐 Frontend Status: RUNNING

- URL: http://localhost:3004
- Console logging: ENABLED

---

## 📋 STEP-BY-STEP TESTING INSTRUCTIONS

### Option 1: Use Browser Console (Recommended)

1. **Open the application**

   - Navigate to: http://localhost:3004
   - You should see the login page

2. **Open Browser DevTools**

   - Press `F12` (or right-click → "Inspect")
   - Click on the **Console** tab

3. **Login and watch logs**

   - Enter credentials:
     - Email: `admin@mikrotik.local`
     - Password: `Admin123!`
   - Click "Sign In"
   - **Watch the Console** for these messages:
     ```
     [Login] Attempting login...
     [API] Login attempt for: admin@mikrotik.local
     [API] Login successful, token received
     [API] Token saved to localStorage
     [Login] Login successful, redirecting...
     ```

4. **Check localStorage**

   - In DevTools, go to **Application** tab
   - Expand **Local Storage** → `http://localhost:3004`
   - You should see: `access_token` with a long JWT string

5. **Navigate to Routers**
   - After login, click on "Routers" in the sidebar
   - **Watch Console** for:
     ```
     [API] Token loaded from localStorage: eyJhbGci...
     [API] Authorization header added
     [API] Calling GET /routers/
     [API] GET /routers/ success: [...]
     ```

---

### Option 2: Fresh Browser (If Still Having Issues)

If you're still seeing "Session expired":

1. **Hard Refresh**

   - Press `Ctrl + Shift + R` (Windows)
   - Or `Ctrl + F5`

2. **Clear Browser Cache**

   - Press `Ctrl + Shift + Delete`
   - Select "Cached images and files"
   - Click "Clear data"

3. **Use Incognito Mode** (GUARANTEED FRESH)

   - Press `Ctrl + Shift + N` (Chrome/Edge)
   - Navigate to http://localhost:3004
   - Login with credentials above

4. **Disable Cache in DevTools**
   - Open DevTools (F12)
   - Go to **Network** tab
   - Check ☑ "Disable cache"
   - Refresh page

---

### Option 3: Test Authentication Page

Visit: **http://localhost:3004/test-auth**

This page will show you:

- ✓/✗ Token exists in localStorage
- ✓/✗ Token is valid (tests /auth/me)
- ✓/✗ /routers/ endpoint accessible
- Raw JSON debug data

---

## 🐛 What to Look For

### ✅ SUCCESS Signs:

- Console shows `[API] Token saved to localStorage`
- Application tab shows `access_token` in localStorage
- Console shows `[API] Authorization header added`
- Routers page loads with router data

### ❌ FAILURE Signs:

- Console shows `[API] No token available - request will fail`
- 401 error in Network tab
- "Session expired" message
- No `access_token` in localStorage

---

## 📝 Troubleshooting

### If token isn't being saved:

1. Check Console for errors during login
2. Make sure localStorage isn't disabled in your browser
3. Try a different browser

### If you see "Session expired":

- This means no token in localStorage
- Either login hasn't completed, or cache is stale
- Use Incognito mode for clean test

### If login fails:

- Check backend is running on port 8001
- Verify credentials: `admin@mikrotik.local` / `Admin123!`
- Check Network tab in DevTools for error details

---

## 🎯 Expected Behavior

**After successful login:**

1. Token saved to localStorage
2. Redirected to home page (/)
3. Can navigate to /routers page
4. Router data loads without errors
5. Console shows all [API] logs with "success" messages

---

## 📞 If Still Not Working

Report these details:

1. Browser name and version
2. Console log output (copy/paste)
3. Network tab errors (if any)
4. localStorage contents (from Application tab)
5. Whether you tried Incognito mode
