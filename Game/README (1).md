# CodeDuel Arena

A full-stack competitive programming platform built with Next.js, FastAPI, and MongoDB.

## Quick Start

### Prerequisites
- Node.js 18+ with yarn
- Python 3.9+ 
- MongoDB running on localhost:27017

### Running the Application

**Option 1: Using the start script (Recommended)**
```bash
cd /app
./start.sh
```

**Option 2: Using npm**
```bash
cd /app
npm run dev
```

This will start:
- Backend API: http://localhost:8001
- Frontend: http://localhost:9002

### First Time Setup

1. **Install Dependencies**
   ```bash
   cd /app
   npm run install-all
   ```

2. **Configure Environment**
   - Backend `.env` is already set up at `/app/backend/.env`
   - Frontend `.env.local` is already set up at `/app/frontend/.env.local`

3. **Start the App**
   ```bash
   npm run dev
   ```

4. **Create an Account**
   - Visit http://localhost:9002
   - Click "Enter the Arena"
   - Sign up with your email

5. **Configure Gemini API Key (Optional)**
   - Get API key from [Google AI Studio](https://aistudio.google.com/apikey)
   - Go to Profile settings
   - Enter your Gemini API key
   - This enables the AI Code Explainer feature

## Features

✅ **Authentication** - Secure JWT-based auth with bcrypt
✅ **User Profiles** - Manage personal info and API keys
✅ **AI Code Explainer** - Get line-by-line code explanations using Gemini 2.5 Flash
✅ **Battle System** - Real-time coding challenges
✅ **Leaderboard** - Track rankings and stats
✅ **Practice Mode** - Sharpen your coding skills

## Documentation

For detailed setup and API documentation, see [README_SETUP.md](/app/README_SETUP.md)

## Tech Stack

- **Frontend**: Next.js 15.3.3, React 18, TypeScript, TailwindCSS
- **Backend**: FastAPI, Python 3.9+
- **Database**: MongoDB
- **Authentication**: JWT with bcrypt
- **AI**: Google Gemini 2.5 Flash
