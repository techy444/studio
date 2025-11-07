#!/bin/bash

# CodeDuel Arena - Start Script
# This script starts both backend and frontend services

echo "🚀 Starting CodeDuel Arena..."
echo ""

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "⚠️  MongoDB is not running. Please start MongoDB first:"
    echo "   sudo service mongodb start"
    exit 1
fi

echo "✓ MongoDB is running"

# Check if we're in the right directory
if [ ! -d "/app/backend" ] || [ ! -d "/app/frontend" ]; then
    echo "❌ Error: Please run this script from /app directory"
    exit 1
fi

echo "✓ Directory structure verified"
echo ""

# Install dependencies if needed
if [ ! -d "/app/frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd /app/frontend && yarn install
fi

echo "✓ Dependencies ready"
echo ""

# Start the application
echo "🎯 Starting services..."
echo "   - Backend: http://localhost:8001"
echo "   - Frontend: http://localhost:9002"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

cd /app && npm run dev
