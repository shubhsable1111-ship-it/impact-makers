# Deployment Guide - LoneGuard AI Credit Risk Assessment

## Overview

This guide provides step-by-step instructions for deploying both the backend (FastAPI + MongoDB) and frontend (HTML/CSS/JS) components of the LoneGuard AI system.

## Project Structure

```
impact-makers/
├── backend/              # FastAPI backend application
│   ├── app/             # Application code
│   ├── requirements.txt # Python dependencies
│   └── test_api.py      # API tests
├── frontend/            # Frontend web application
│   ├── index.html       # Entry point
│   ├── css/            # Stylesheets
│   └── js/             # JavaScript modules
├── README.md           # Main documentation
└── DEPLOYMENT.md       # This file
```

## Backend Deployment

### Prerequisites

- Python 3.9 or higher
- MongoDB instance (local or cloud like MongoDB Atlas)
- Environment variables configuration

### Option 1: Deploy to Render (Recommended)

1. **Prepare Backend**:
   ```bash
   # Ensure all dependencies are listed
   cd backend
   pip freeze > requirements.txt
   ```

2. **Create Render Account**: Sign up at [render.com](https://render.com)

3. **Create New Web Service**:
   - Connect your GitHub repository
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables** (in Render dashboard):
   ```
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/credit_risk_db
   PYTHON_VERSION=3.13.1
   ```

5. **Deploy**: Click "Create Web Service"

### Option 2: Deploy to Railway

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and Initialize**:
   ```bash
   railway login
   cd backend
   railway init
   ```

3. **Add MongoDB**:
   ```bash
   railway add mongodb
   ```

4. **Deploy**:
   ```bash
   railway up
   ```

### Option 3: Docker Deployment

1. **Create Dockerfile** in `backend/`:
   ```dockerfile
   FROM python:3.13-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 8000
   
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Build and Run**:
   ```bash
   cd backend
   docker build -t loneguard-backend .
   docker run -p 8000:8000 -e MONGODB_URL="your_mongodb_url" loneguard-backend
   ```

## Frontend Deployment

### Option 1: Netlify (Recommended)

1. **Install Netlify CLI**:
   ```bash
   npm install -g netlify-cli
   ```

2. **Deploy**:
   ```bash
   cd frontend
   netlify deploy --prod --dir .
   ```

3. **Update API URL** in `js/api.js`:
   ```javascript
   const BASE_URL = "https://your-backend.onrender.com";
   ```

### Option 2: Vercel

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy**:
   ```bash
   cd frontend
   vercel --prod
   ```

### Option 3: GitHub Pages

1. **Enable GitHub Pages** in repository settings
2. **Select Source**: Deploy from `main` branch / `frontend` folder
3. **Update API_URL** before pushing

### Option 4: AWS S3 + CloudFront

1. **Create S3 Bucket**:
   - Enable static website hosting
   - Upload frontend files

2. **Create CloudFront Distribution**:
   - Point to S3 bucket
   - Enable HTTPS

## MongoDB Setup

### MongoDB Atlas (Cloud - Recommended)

1. **Create Account**: Sign up at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)

2. **Create Cluster**:
   - Choose free tier (M0)
   - Select region closest to your backend server

3. **Create Database User**:
   - Username: `loneguard_user`
   - Password: Generate strong password
   - Privileges: Read and write to any database

4. **Whitelist IP Addresses**:
   - For development: Add your current IP
   - For production: Add `0.0.0.0/0` (allow all) or your server's IP

5. **Get Connection String**:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/credit_risk_db?retryWrites=true&w=majority
   ```

### Local MongoDB

1. **Install MongoDB**:
   - Windows: Download from [mongodb.com](https://www.mongodb.com/try/download/community)
   - Mac: `brew install mongodb-community`
   - Linux: Follow [official guide](https://docs.mongodb.com/manual/installation/)

2. **Start MongoDB**:
   ```bash
   mongod --dbpath /path/to/data
   ```

3. **Connection String**:
   ```
   MONGODB_URL=mongodb://localhost:27017
   ```

## Environment Variables

### Backend (.env file)

Create `backend/.env`:
```env
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/credit_risk_db
DATABASE_NAME=credit_risk_db
```

### Frontend (js/api.js)

Update `BASE_URL` for production:
```javascript
const BASE_URL = "https://your-deployed-backend.com";
```

## Testing Deployment

### Backend Health Check

```bash
curl https://your-backend-url.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### Frontend Test

1. Open frontend URL in browser
2. Click "Borrower" → should navigate to registration
3. Fill form and submit → should call backend API
4. Check browser DevTools → Network tab for API calls

## Troubleshooting

### Backend Issues

**Error: Cannot connect to MongoDB**
- Check `MONGODB_URL` environment variable
- Verify MongoDB Atlas IP whitelist
- Ensure database user has correct permissions

**Error: Module not found**
- Run `pip install -r requirements.txt`
- Check Python version (3.9+)

### Frontend Issues

**CORS Error**
- Ensure backend has CORS middleware enabled
- Check `allow_origins` in `backend/app/main.py`

**API calls fail**
- Verify `BASE_URL` in `frontend/js/api.js`
- Check backend is running and accessible
- Inspect browser console for errors

## Production Checklist

- [ ] Backend deployed and accessible
- [ ] MongoDB database created and accessible
- [ ] Environment variables configured
- [ ] Frontend deployed
- [ ] Frontend `BASE_URL` updated to production backend
- [ ] CORS configured correctly
- [ ] SSL/HTTPS enabled for both frontend and backend
- [ ] Test registration flow end-to-end
- [ ] Test credit score calculation
- [ ] Monitor logs for errors

## Monitoring

### Backend Logs

**Render**: View logs in dashboard
**Railway**: `railway logs`
**Docker**: `docker logs <container_id>`

### Frontend

- Use browser DevTools Console
- Set up error tracking (e.g., Sentry)

## Support

For issues or questions, refer to:
- Backend README: `backend/README.md`
- Frontend README: `frontend/README.md`
- Main README: `README.md`
