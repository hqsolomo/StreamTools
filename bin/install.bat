@echo off

REM Install Python
echo Installing Python...
choco install python --version 3.11.4 -y

REM Add Python to PATH
echo Adding Python to PATH...
setx PATH "%PATH%;C:\Python3114" /M

REM Install Pillow
echo Installing Pillow...
pip install pillow

echo Installation complete.
pause
