import gradio as gr
import tempfile
import shutil
from pathlib import Path
import os
from src.preprocess_videos import preprocess_videos
import click

def process_videos(
    input_files,
    target_duration: float = 2.5,
    target_width: int = 848,
    target_height: int = 480,
    target_fps: int = 30,
    progress=gr.Progress(track_tqdm=True)
):
    """
    Process uploaded videos using the existing preprocessor logic
    with additional parameters for resolution and framerate
    """
    # Create temporary directories for processing
    with tempfile.TemporaryDirectory() as input_dir, \
         tempfile.TemporaryDirectory() as output_dir:
        
        # Save uploaded files to input directory
        input_path = Path(input_dir)
        for file in input_files:
            shutil.copy(file.name, input_path)
        
        # Process videos using existing logic with new parameters
        preprocess_videos.callback(
            input_folder=str(input_path),
            output_folder=output_dir,
            duration=target_duration,
            width=target_width,
            height=target_height,
            fps=target_fps
        )
        
        # Collect all processed files
        output_files = []
        output_path = Path(output_dir)
        for ext in ['.mp4', '.txt']:
            output_files.extend(list(output_path.rglob(f'*{ext}')))
            
        # Create a zip file containing all outputs
        zip_path = tempfile.mktemp(suffix='.zip')
        shutil.make_archive(zip_path[:-4], 'zip', output_dir)
        
        return zip_path

# Create the Gradio interface
demo = gr.Interface(
    fn=process_videos,
    inputs=[
        gr.File(
            file_count="multiple",
            label="Upload Videos",
            file_types=["avi", "mp4", "mov"]
        ),
        gr.Slider(
            minimum=1.0,
            maximum=5.0,
            value=2.5,
            step=0.5,
            label="Target Duration (seconds)",
            info="Length of each video segment"
        ),
        gr.Number(
            value=848,
            minimum=320,
            maximum=1920,
            step=16,
            label="Target Width",
            info="Output video width in pixels"
        ),
        gr.Number(
            value=480,
            minimum=240,
            maximum=1080,
            step=16,
            label="Target Height",
            info="Output video height in pixels"
        ),
        gr.Slider(
            minimum=15,
            maximum=60,
            value=30,
            step=1,
            label="Target FPS",
            info="Output video framerate"
        )
    ],
    outputs=gr.File(
        label="Download Processed Videos",
        file_count="single",
        type="filepath"
    ),
    title="Mochi-1 Video Preprocessor",
    description="""
    This tool helps prepare videos for Mochi-1 model training by:
    - Splitting videos into segments of specified duration
    - Standardizing resolution to desired dimensions
    - Converting to specified framerate
    - Creating caption placeholder files
    """,
    article="""
    ## Processing Details
    
    Your videos will be:
    1. Split into segments of the specified duration
    2. Resized to the target resolution
    3. Converted to the target framerate
    4. Stripped of audio (not needed for training)
    
    For each video segment, you'll get:
    - A processed MP4 file
    - A corresponding .txt file for captions
    
    All files will be returned in a single ZIP archive.
    """,
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    demo.launch()  # Now only accessible locally