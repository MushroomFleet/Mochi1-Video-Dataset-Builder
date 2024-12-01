# Video Captioner Project Manifest

## Project Root Level Files
- `install.bat` -> From artifact: "video-caption-install"
- `start.bat` -> From artifact: "video-caption-start"
- `preprocess_videos.bat` -> From artifact: "preprocess-videos"
- `requirements.txt` -> From artifact: "video-caption-requirements"
- `README.md` -> From artifact: "video-caption-readme"
- `.gitignore` -> From artifact: "video-caption-gitignore"

## Directory Structure
```
project_root/
├── models/               # Create this directory (empty initially)
│   └── [place llava-v1.5-7b-q4.gguf here after downloading]
├── src/
│   ├── __init__.py      -> From artifact: "video-captioner-init"
│   ├── video_captioner.py   -> From artifact: "local-video-captioner"
│   └── preprocess_videos.py -> From artifact: "video-preprocessor"
├── install.bat
├── start.bat
├── preprocess_videos.bat
├── requirements.txt
├── README.md
└── .gitignore
```

## File Creation Order
1. Create root directory
2. Create `models` subdirectory
3. Create `src` subdirectory
4. Copy each file from its artifact to the corresponding location above
5. Download LLaVA model and place in models directory (post-setup)

## Video Processing Pipeline
1. Run `preprocess_videos.bat` to:
   - Split videos into 2.5s segments
   - Standardize to 848x480 resolution
   - Convert to 30fps
   - Generate placeholder caption files
2. Run `start.bat` to generate captions for processed videos

## Important Notes
- The `models` directory should be created but will be empty initially
- The LLaVA model file needs to be downloaded separately
- All Python files should maintain their `.py` extension
- Maintain exact filenames as shown in the structure
- Video preprocessing must be completed before captioning
- Processing supports both MP4 and MOV input formats