@echo off
echo Video Preprocessor for Mochi-1 Training
echo =====================================
echo.

rem Activate virtual environment
call venv\Scripts\activate.bat

rem Check if required packages are installed
python -c "import moviepy" 2>NUL
if errorlevel 1 (
    echo Installing required packages...
    pip install moviepy tqdm
)

:input_paths
echo Please enter the following paths:
echo.
set /p input_folder="Input folder containing videos: "
set /p output_folder="Output folder for processed videos: "

if not exist "%input_folder%" (
    echo Error: Input folder does not exist!
    goto input_paths
)

echo.
echo Processing videos...
echo Input: %input_folder%
echo Output: %output_folder%
echo.

python src\preprocess_videos.py "%input_folder%" "%output_folder%" -d 2.5

echo.
echo Press any key to exit...
pause