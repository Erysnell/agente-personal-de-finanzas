@echo off
REM Setup script for Personal Finance Agent (Windows)
echo Setting up Personal Finance Agent...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

echo Python detected

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

if %errorlevel% neq 0 (
    echo Error: Could not create virtual environment
    exit /b 1
)

echo Virtual environment created

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error installing dependencies
    exit /b 1
)

echo Dependencies installed successfully

REM Create .env file if it doesn't exist
echo.
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo .env file created
    echo.
    echo IMPORTANT: Please edit the .env file and add your API keys:
    echo    1. TELEGRAM_BOT_TOKEN - Get from @BotFather on Telegram
    echo    2. GOOGLE_API_KEY - Get from https://makersuite.google.com/app/apikey
    echo.
) else (
    echo .env file already exists
)

REM Run tests
echo.
echo Running tests...
python test.py

if %errorlevel% equ 0 (
    echo.
    echo Setup completed successfully!
    echo.
    echo Next steps:
    echo 1. Edit the .env file with your API keys
    echo 2. Activate the virtual environment: venv\Scripts\activate
    echo 3. Run the bot: python bot.py
) else (
    echo.
    echo Setup completed with test warnings
    echo Please check the output above for details
)
