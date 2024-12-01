@echo off
echo Starting Video Preprocessor Web Interface
echo =====================================
echo.

rem Activate virtual environment
call venv\Scripts\activate.bat

rem Check if gradio is installed
python -c "import gradio" 2>NUL
if errorlevel 1 (
    echo Installing Gradio and dependencies...
    pip install -r requirements.txt
)

echo.
echo Starting web interface...
echo.
echo Once the server starts, open your web browser to the URL shown
echo Press Ctrl+C to stop the server when finished
echo.

python -m src.gradio_app

echo.
echo Press any key to exit...
pause
