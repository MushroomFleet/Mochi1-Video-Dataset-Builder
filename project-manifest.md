# Video Preprocessor Project Manifest

## Project Root Level Files
- `install.bat` -> From artifact: "video-preprocess-install"
- `preprocess_videos.bat` -> From artifact: "preprocess-videos"
- `start_preprocessor_ui.bat` -> From artifact: "preprocess-ui-start"
- `requirements.txt` -> From artifact: "video-preprocess-requirements"
- `README.md` -> From artifact: "video-preprocess-readme"
- `.gitignore` -> From artifact: "video-preprocess-gitignore"

## Directory Structure
```
project_root/
├── src/
│   ├── __init__.py      -> From artifact: "video-preprocessor-init"
│   ├── preprocess_videos.py -> From artifact: "video-preprocessor"
│   └── gradio_app.py    -> From artifact: "video-preprocessor-ui"
├── install.bat
├── preprocess_videos.bat
├── start_preprocessor_ui.bat
├── requirements.txt
├── README.md
└── .gitignore
```

## File Creation Order
1. Create root directory
2. Create `src` subdirectory
3. Copy each file from its artifact to the corresponding location above

## Video Processing Pipeline
1. Run `preprocess_videos.bat` to:
   - Split videos into 2.5s segments
   - Standardize to 848x480 resolution
   - Convert to 30fps
   - Generate placeholder caption files

## Important Notes
- All Python files should maintain their `.py` extension
- Maintain exact filenames as shown in the structure
- Video preprocessing must be completed before training
- Processing supports both MP4 and MOV input formats
