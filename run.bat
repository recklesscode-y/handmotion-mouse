@echo off

cd /d "%~dp0"

if not exist handmotion_mouse (
echo Virtual environment not found.
echo Please run setup.bat first.
pause
exit /b
)

call handmotion_mouse\Scripts\activate

python hand_trackv6.py

pause
