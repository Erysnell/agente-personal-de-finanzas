#!/bin/bash

# Setup script for Personal Finance Agent
echo "🚀 Setting up Personal Finance Agent..."

# Check if Python 3.8+ is installed
python_version=$(python3 --version 2>&1 | grep -oP '(?<=Python )\d+\.\d+')
major=$(echo $python_version | cut -d. -f1)
minor=$(echo $python_version | cut -d. -f2)

if [ "$major" -lt 3 ] || ([ "$major" -eq 3 ] && [ "$minor" -lt 8 ]); then
    echo "❌ Error: Python 3.8 or higher is required"
    exit 1
fi

echo "✓ Python $python_version detected"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✓ Virtual environment created"
echo ""
echo "🔧 Activating virtual environment..."

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo "❌ Error: Could not find virtual environment activation script"
    exit 1
fi

echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Error installing dependencies"
    exit 1
fi

# Create .env file if it doesn't exist
echo ""
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit the .env file and add your API keys:"
    echo "   1. TELEGRAM_BOT_TOKEN - Get from @BotFather on Telegram"
    echo "   2. GOOGLE_API_KEY - Get from https://makersuite.google.com/app/apikey"
    echo ""
else
    echo "✓ .env file already exists"
fi

# Run tests
echo ""
echo "🧪 Running tests..."
python test.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Edit the .env file with your API keys"
    echo "2. Activate the virtual environment:"
    echo "   source venv/bin/activate   (Linux/Mac)"
    echo "   venv\\Scripts\\activate      (Windows)"
    echo "3. Run the bot:"
    echo "   python bot.py"
else
    echo ""
    echo "⚠️  Setup completed with test warnings"
    echo "Please check the output above for details"
fi
