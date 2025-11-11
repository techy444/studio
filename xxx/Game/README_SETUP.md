# CodeDuel Arena - Setup & Running Guide

## Project Structure

```
/app/
├── backend/          # FastAPI backend (Python)
│   ├── server.py     # Main API server
│   ├── database.py   # MongoDB configuration
│   ├── auth_utils.py # JWT authentication
│   └── .env          # Backend environment variables
├── frontend/         # Next.js frontend (React/TypeScript)
│   ├── src/          # Source code
│   └── .env.local    # Frontend environment variables
└── package.json      # Root package.json for running both services
```

## Prerequisites

- Python 3.9+ with pip
- Node.js 18+ with yarn
- MongoDB running on localhost:27017

## Installation

### Backend Setup
```bash
cd /app/backend
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd /app/frontend
yarn install
```

## Running the Application

### Option 1: Run Both Services Together (Recommended)
From the root directory `/app`:
```bash
npm run dev
```
This will start:
- Backend API on http://localhost:8001
- Frontend on http://localhost:9002

### Option 2: Run Services Separately

**Terminal 1 - Backend:**
```bash
cd /app
npm run backend
```

**Terminal 2 - Frontend:**
```bash
cd /app
npm run frontend
```

## Environment Variables

### Backend (.env)
Located at `/app/backend/.env`:
```env
MONGO_URL=mongodb://localhost:27017
MONGO_DB_NAME=codeduel_arena
SECRET_KEY=codeduel-super-secret-key-change-in-production-2024
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

### Frontend (.env.local)
Located at `/app/frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8001
```

## Features

1. **Authentication**
   - Sign up / Sign in at `/login`
   - JWT-based authentication
   - Secure password hashing with bcrypt

2. **User Profile**
   - Update name and personal information
   - Configure Gemini API key for AI features
   - View stats (points, wins, losses)

3. **AI Code Explainer**
   - Requires Gemini API key (configure in profile)
   - Uses gemini-2.5-flash model
   - Line-by-line code explanations
   - Automatic retry logic with exponential backoff

4. **Battle System**
   - Real-time coding battles
   - Timer-based challenges
   - Leaderboard tracking

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### Profile
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update profile (name, gemini_api_key)

### Battle
- `POST /api/battle/start` - Start new battle
- `POST /api/battle/timeout` - Handle battle timeout

### AI Features
- `POST /api/explainer/explain` - Explain code snippet (requires Gemini API key)

## Getting Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key
5. Go to your profile settings in CodeDuel Arena
6. Paste the API key in the "Gemini API Key" field
7. Click "Save Changes"

## Testing the Backend

```bash
# Health check
curl http://localhost:8001/

# Create account
curl -X POST http://localhost:8001/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "pass123", "username": "coder123"}'

# Login
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "pass123"}'

# Get profile (replace TOKEN with your JWT)
curl http://localhost:8001/api/profile \
  -H "Authorization: Bearer TOKEN"

# Update profile
curl -X PUT http://localhost:8001/api/profile \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"name": "John Doe", "gemini_api_key": "your-api-key"}'
```

## Troubleshooting

### Backend not starting
```bash
# Check if MongoDB is running
ps aux | grep mongod

# Check backend logs
tail -f /var/log/supervisor/backend.err.log

# Check if port 8001 is in use
lsof -i :8001
```

### Frontend not starting
```bash
# Reinstall dependencies
cd /app/frontend
rm -rf node_modules yarn.lock
yarn install

# Check if port 9002 is in use
lsof -i :9002
```

### Database connection issues
```bash
# Start MongoDB
sudo service mongodb start

# Or if using systemd
sudo systemctl start mongodb
```

### "Please configure your Gemini API key" error
1. Go to http://localhost:9002/profile
2. Enter your Gemini API key (get it from https://aistudio.google.com/apikey)
3. Click "Save Changes"
4. Try the AI Code Explainer feature again

## Development Workflow

1. Start the application with `npm run dev` from `/app`
2. Access frontend at http://localhost:9002
3. Backend API at http://localhost:8001
4. Make changes to code (both frontend and backend support hot reload)
5. Changes will automatically reflect in the browser

## Production Deployment

For production, you'll need to:
1. Build the frontend: `cd frontend && yarn build`
2. Update environment variables for production URLs
3. Use a process manager like PM2 or supervisor
4. Set up reverse proxy with nginx
5. Enable HTTPS with SSL certificates
6. Use a production-grade MongoDB instance

## Tech Stack

- **Frontend**: Next.js 15.3.3, React 18, TypeScript, TailwindCSS
- **Backend**: FastAPI, Python 3.9+
- **Database**: MongoDB
- **Authentication**: JWT with bcrypt
- **AI**: Google Gemini 2.5 Flash

## Support

For issues or questions:
- Check the logs in `/var/log/supervisor/`
- Review API documentation at http://localhost:8001/docs
- Ensure all environment variables are correctly set
