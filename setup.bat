@echo off

cd /d "%~dp0"

echo ======================================
echo HandMotion Mouse Setup
echo ======================================
echo.

if exist handmotion_mouse (
echo Virtual environment already exists.
pause
exit /b
)

echo Creating virtual environment...
python -m venv handmotion_mouse

call handmotion_mouse\Scripts\activate

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ======================================
echo Setup Complete
echo ======================================
echo.
echo Run run.bat to start the application.
echo.

pause
