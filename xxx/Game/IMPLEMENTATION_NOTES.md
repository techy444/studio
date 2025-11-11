# CodeDuel Arena - Implementation Notes

## Overview
This document describes the implementation of authentication, battle timer updates, and loading states for the CodeDuel Arena application.

## Tech Stack
- **Frontend**: Next.js 15.3.3 (running on port 9002)
- **Backend**: FastAPI (running on port 8001)
- **Database**: MongoDB (running on localhost:27017)
- **Authentication**: JWT with bcrypt password hashing

## What Was Implemented

### 1. Backend API (FastAPI + MongoDB)

#### Directory Structure
```
/app/backend/
├── server.py        # Main FastAPI application
├── database.py      # MongoDB connection and collections
├── auth_utils.py    # JWT and password hashing utilities
├── requirements.txt # Python dependencies
└── .env            # Environment variables
```

#### API Endpoints
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info (requires JWT)
- `POST /api/battle/timeout` - Handle battle timeout (requires JWT)
- `POST /api/battle/start` - Start a new battle (requires JWT)

#### MongoDB Collections
- **users**: Stores user accounts with hashed passwords
  ```json
  {
    "_id": "uuid",
    "username": "string",
    "email": "string",
    "hashed_password": "string",
    "created_at": "datetime",
    "total_points": 0,
    "wins": 0,
    "losses": 0
  }
  ```

- **battles**: Stores battle information
  ```json
  {
    "battle_id": "string",
    "start_time": "datetime",
    "end_time": "datetime",
    "status": "active|timeout|completed",
    "player1_id": "string",
    "player2_id": "string",
    "winner_id": "string"
  }
  ```

### 2. Authentication System

#### Login/Signup Page
- Location: `/app/src/app/auth/login/page.tsx`
- Features:
  - Email and password authentication
  - Toggle between login and signup modes
  - Loading states during authentication
  - Error handling with toast notifications
  - Auto-redirect if already logged in
  - Consistent theme with existing UI

#### Auth Utilities
- Location: `/app/src/lib/auth.ts`
- Functions:
  - `getAuthToken()` - Retrieve JWT from localStorage
  - `getAuthUser()` - Get user data from localStorage
  - `setAuthData()` - Store authentication data
  - `clearAuthData()` - Remove authentication data
  - `isAuthenticated()` - Check authentication status
  - `authenticatedFetch()` - Make authenticated API calls

#### User Navigation
- Updated `/app/src/components/layout/user-nav.tsx`
- Shows "Sign In" button when logged out
- Shows user avatar and info when logged in
- Logout functionality clears session and redirects to login

### 3. Battle Timer Update

#### Changes
- **Old Timer**: 5 minutes (300 seconds)
- **New Timer**: 30 minutes (1800 seconds)
- Location: `/app/src/app/(app)/battle/[matchId]/page.tsx`

#### Auto-Timeout Feature
When the timer reaches zero:
1. Calls `POST /api/battle/timeout` with battle ID
2. Displays toast notification: "Time's Up!"
3. Redirects to battle lobby after 2 seconds

### 4. Loading States

#### Loading Component
- Location: `/app/src/components/ui/loading.tsx`
- Two variants:
  - `Loading` - Inline loading for page sections
  - `LoadingFullscreen` - Full-screen loading overlay

#### Usage
- Battle page: Shows "Connecting to Arena..." during auth check
- Login page: Shows spinner during authentication
- Consistent loading animations with Lucide icons

### 5. Protected Routes

- All app pages check for authentication
- Redirect to `/auth/login` if not authenticated
- Home page "Enter Arena" button points to login page

## Environment Variables

### Backend (.env)
```env
MONGO_URL=mongodb://localhost:27017
MONGO_DB_NAME=codeduel_arena
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8001
```

## Testing the Implementation

### 1. Test Backend API
```bash
# Health check
curl http://localhost:8001/

# Signup
curl -X POST http://localhost:8001/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "pass123", "username": "testuser"}'

# Login
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "pass123"}'

# Get current user (replace TOKEN with actual JWT)
curl http://localhost:8001/api/auth/me \
  -H "Authorization: Bearer TOKEN"
```

### 2. Test Frontend
1. Navigate to `http://localhost:9002`
2. Click "Enter the Arena"
3. Sign up with email and password
4. You'll be redirected to the practice page
5. Go to Battle page - should show "Connecting to Arena..." briefly
6. In battle room, timer should show 30:00 initially

### 3. Test Battle Timeout
1. Start a battle
2. Wait for timer to reach 00:00
3. Should see "Time's Up!" notification
4. Should redirect to battle lobby

## Services

### Start/Stop Services
```bash
# Backend
supervisorctl restart backend

# MongoDB (already running)
ps aux | grep mongod

# Frontend (running in background)
cd /app && npm run dev
```

### Check Logs
```bash
# Backend logs
tail -f /var/log/supervisor/backend.out.log
tail -f /var/log/supervisor/backend.err.log

# Frontend logs
tail -f /var/log/frontend.log
```

## Security Notes

1. **JWT Tokens**: Expire after 7 days by default
2. **Password Hashing**: Uses bcrypt with salt
3. **CORS**: Configured for localhost:3000 and localhost:9002
4. **Environment Variables**: Never commit .env files to git

## Future Enhancements

1. Add password strength validation
2. Implement "Remember Me" functionality
3. Add email verification
4. Add password reset functionality
5. Implement real-time battle synchronization
6. Add battle history and statistics
7. Implement WebSocket for live opponent progress

## Troubleshooting

### Backend not starting
```bash
# Check if port 8001 is in use
lsof -i :8001

# Check MongoDB connection
mongo --eval "db.serverStatus()"

# View backend logs
tail -50 /var/log/supervisor/backend.err.log
```

### Frontend not loading
```bash
# Check if port 9002 is in use
lsof -i :9002

# Reinstall dependencies
cd /app && npm install

# Check frontend logs
tail -50 /var/log/frontend.log
```

### MongoDB issues
```bash
# Check if MongoDB is running
ps aux | grep mongod

# Check MongoDB logs
tail -50 /var/log/mongodb.log
```

## File Changes Summary

### New Files
- `/app/backend/` (entire directory)
- `/app/src/app/auth/login/page.tsx`
- `/app/src/lib/auth.ts`
- `/app/src/components/ui/loading.tsx`
- `/app/.env.local`
- `/etc/supervisor/conf.d/backend.conf`

### Modified Files
- `/app/src/app/page.tsx`
- `/app/src/app/(app)/battle/page.tsx`
- `/app/src/app/(app)/battle/[matchId]/page.tsx`
- `/app/src/components/layout/user-nav.tsx`

## Contact & Support

For issues or questions about this implementation, refer to:
- FastAPI docs: https://fastapi.tiangolo.com/
- Next.js docs: https://nextjs.org/docs
- MongoDB docs: https://docs.mongodb.com/
