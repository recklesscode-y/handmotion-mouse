@echo off

echo ======================================
echo HandMotion Mouse Setup
echo ======================================
echo.

echo Creating virtual environment...
python -m venv handmotion_mouse

echo.
echo Activating virtual environment...
call handmotion_mouse\Scripts\activate

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ======================================
echo Setup Complete
echo ======================================
echo.
echo To start the application, run:
echo run.bat
echo.

pause
