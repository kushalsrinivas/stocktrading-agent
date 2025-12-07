#!/bin/bash

# Startup script for Stock Backtesting API

echo "========================================================================"
echo "   🚀 STARTING STOCK BACKTESTING API SERVER"
echo "========================================================================"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  No virtual environment found. Using system Python."
fi

# Check if required packages are installed
echo "🔍 Checking dependencies..."
python -c "import fastapi, uvicorn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Required packages not found."
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

echo ""
echo "✅ All dependencies OK"
echo ""
echo "========================================================================"
echo "   Starting API Server..."
echo "========================================================================"
echo ""
echo "   📊 22 Trading Strategies Available"
echo "   🔥 Advanced S/R Strategies Included"
echo ""
echo "   Server URL:  http://localhost:8000"
echo "   API Docs:    http://localhost:8000/docs"
echo "   Health:      http://localhost:8000/health"
echo ""
echo "========================================================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python api_server.py

