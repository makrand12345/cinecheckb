# Fix MongoDB Atlas SSL Connection Error

## The Problem

You're seeing this error:
```
SSL handshake failed: [SSL: TLSV1_ALERT_INTERNAL_ERROR] tlsv1 alert internal error
```

**This is 99% of the time caused by MongoDB Atlas Network Access restrictions.**

## Step-by-Step Fix

### Step 1: Log into MongoDB Atlas
1. Go to https://cloud.mongodb.com
2. Log in with your MongoDB Atlas account

### Step 2: Navigate to Network Access
1. In the left sidebar, click **"Network Access"** (under Security)
2. You should see a list of IP addresses or "0.0.0.0/0" if already configured

### Step 3: Add IP Address
1. Click the **"Add IP Address"** button (green button, top right)
2. You have two options:

   **Option A (Recommended for Development):**
   - Click **"Allow Access from Anywhere"**
   - This automatically adds `0.0.0.0/0`
   - Click **"Confirm"**
   
   **Option B (More Secure for Production):**
   - Enter `0.0.0.0/0` manually
   - Add a comment like "Render deployment"
   - Click **"Confirm"**

### Step 4: Wait for Propagation
- MongoDB Atlas needs 1-3 minutes to propagate the network access changes
- You'll see a status indicator showing when it's active

### Step 5: Verify Your Connection String
1. Go to MongoDB Atlas → **"Database"** (left sidebar)
2. Click **"Connect"** on your cluster
3. Choose **"Connect your application"**
4. Copy the connection string - it should look like:
   ```
   mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
   ```
5. **Important**: 
   - Replace `<username>` and `<password>` with your actual credentials
   - If your password contains special characters (`@`, `:`, `/`, `#`, etc.), you MUST URL-encode them:
     - `@` becomes `%40`
     - `:` becomes `%3A`
     - `/` becomes `%2F`
     - `#` becomes `%23`
     - Space becomes `%20`

### Step 6: Update Render Environment Variable
1. Go to your Render dashboard
2. Navigate to your service
3. Go to **"Environment"** tab
4. Find the `MONGODB_URI` variable
5. Update it with your connection string (make sure it's correct)
6. Save the changes

### Step 7: Restart Render Service
1. In Render dashboard, go to **"Manual Deploy"** or **"Events"**
2. Click **"Deploy latest commit"** or **"Restart"**
3. Wait for the deployment to complete

### Step 8: Check Logs
1. In Render dashboard, go to **"Logs"** tab
2. Look for:
   - ✅ `MongoDB connected and Beanie initialized` (success!)
   - ❌ `SSL handshake failed` (still an issue)

## Common Issues

### Issue: Still getting SSL errors after adding 0.0.0.0/0
**Solution:**
- Wait 3-5 minutes for MongoDB Atlas to fully propagate the changes
- Double-check that the IP address was actually added (should show in the Network Access list)
- Verify your connection string is correct in Render environment variables
- Try restarting the Render service again

### Issue: Connection string has special characters
**Solution:**
- URL-encode special characters in your password
- Example: If password is `p@ssw:rd`, use `p%40ssw%3Ard` in the connection string
- Or change your MongoDB user password to one without special characters

### Issue: "Authentication failed" error
**Solution:**
- Check your MongoDB Atlas Database Access (Users)
- Ensure the user exists and has the correct permissions
- Verify the username and password in your connection string

## Verification

Once fixed, you should see in Render logs:
```
🔌 Connecting to MongoDB...
   URI format: mongodb+srv://
   Database: cinecheck
   Testing connection...
   ✅ Connection successful!
✅ MongoDB connected and Beanie initialized
```

And your API will start returning real data instead of mock data!

## Still Having Issues?

If you've followed all steps and still see SSL errors:
1. Check MongoDB Atlas status page for any outages
2. Verify your MongoDB Atlas cluster is running (not paused)
3. Try creating a new database user with a simple password (no special chars)
4. Check Render's status page for any issues

