@echo off
REM Quick setup script for Railway deployment (Windows)

echo.
echo 🚀 Animal Rescue - Railway Deployment Setup
echo ==============================================
echo.

REM Check if Railway CLI is installed
railway --version >nul 2>&1
if errorlevel 1 (
    echo Installing Railway CLI...
    echo Download from: https://railway.app/dashboard
    echo Then run: npm install -g @railway/cli
    echo.
)

REM Generate SECRET_KEY
echo Generating Django SECRET_KEY...
python -c "from django.core.management.utils import get_random_secret_key; print(f'SECRET_KEY={get_random_secret_key()}')" > temp_key.txt
for /f "tokens=2 delims==" %%A in (temp_key.txt) do set SECRET_KEY=%%A
del temp_key.txt
echo Generated SECRET_KEY: %SECRET_KEY%

REM Create .env file
echo.
echo Creating .env file...
copy .env.example .env

REM Update SECRET_KEY in .env (using PowerShell)
powershell -Command "(Get-Content .env) -replace 'your-secret-key-here-change-in-production', '%SECRET_KEY%' | Set-Content .env"

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Update .env with your ALLOWED_HOSTS domain
echo 2. Commit and push to GitHub:
echo    git add .
echo    git commit -m "Add Railway deployment configuration"
echo    git push
echo 3. Go to Railway dashboard: https://railway.app/dashboard
echo 4. Create new project from your GitHub repository
echo 5. Add PostgreSQL plugin and configure environment variables
echo 6. Watch the deployment logs!
echo.
echo 📖 See RAILWAY_DEPLOYMENT.md for detailed instructions
echo.
pause
