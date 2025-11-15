# Deploying to Render

This guide will help you deploy the CineCheck backend to Render.

## Prerequisites

1. A Render account (sign up at https://render.com)
2. A MongoDB database (MongoDB Atlas recommended)
3. Your repository pushed to GitHub/GitLab/Bitbucket

## Deployment Steps

### Option 1: Using Render Blueprint (Recommended)

1. Go to your Render dashboard
2. Click "New" → "Blueprint"
3. Connect your repository
4. Render will automatically detect the `render.yaml` file
5. Review the configuration and click "Apply"

### Option 2: Manual Setup

1. Go to your Render dashboard
2. Click "New" → "Web Service"
3. Connect your repository
4. Configure the service:
   - **Name**: `cinecheck-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn src.app:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
   - **Root Directory**: `cineckeckb` (or the path to your backend folder)

5. Add Environment Variables:
   - `MONGODB_URI`: Your MongoDB connection string
   - `DB_NAME`: `cinecheck` (or your preferred database name)
   - `JWT_SECRET`: A secure random string (Render can generate this)
   - `JWT_ALGORITHM`: `HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: `60`
   - `CORS_ORIGINS`: `https://cinecheckf.vercel.app,http://localhost:4200` (comma-separated)
   - `PORT`: Automatically set by Render (don't override)

6. Click "Create Web Service"

## Environment Variables

Make sure to set these environment variables in your Render dashboard:

- **MONGODB_URI** (Required): Your MongoDB Atlas connection string
- **DB_NAME**: Database name (default: `cinecheck`)
- **JWT_SECRET** (Required): Secret key for JWT tokens
- **JWT_ALGORITHM**: Algorithm for JWT (default: `HS256`)
- **ACCESS_TOKEN_EXPIRE_MINUTES**: Token expiration time (default: `60`)
- **CORS_ORIGINS**: Comma-separated list of allowed origins

## Post-Deployment

1. After deployment, your API will be available at: `https://your-service-name.onrender.com`
2. Test the root endpoint: `https://your-service-name.onrender.com/`
3. Update your frontend CORS settings if needed
4. Update your frontend API base URL to point to the Render URL

## Troubleshooting

- **Build fails**: Check that all dependencies in `requirements.txt` are correct
- **App crashes**: Check the logs in Render dashboard for error messages
- **Database connection fails**: Verify your `MONGODB_URI` is correct and MongoDB Atlas allows connections from Render's IPs (0.0.0.0/0)
- **CORS errors**: Make sure your frontend URL is included in `CORS_ORIGINS`

## Notes

- Render provides a free tier with some limitations (service may spin down after inactivity)
- For production, consider upgrading to a paid plan
- The service automatically restarts on code pushes if auto-deploy is enabled

