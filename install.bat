@echo off
echo Creating Python virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Installation complete! You can now use the video captioner.
echo To activate the environment in the future, run: venv\Scripts\activate.bat

pause
