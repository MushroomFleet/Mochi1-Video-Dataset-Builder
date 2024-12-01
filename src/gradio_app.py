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
    progress=gr.Progress(track_tqdm=True)
):
    """
    Process uploaded videos using the existing preprocessor logic
    """
    # Create temporary directories for processing
    with tempfile.TemporaryDirectory() as input_dir, \
         tempfile.TemporaryDirectory() as output_dir:
        
        # Save uploaded files to input directory
        input_path = Path(input_dir)
        for file in input_files:
            shutil.copy(file.name, input_path)
        
        # Process videos using existing logic
        preprocess_videos.callback(
            input_folder=str(input_path),
            output_folder=output_dir,
            duration=target_duration
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
            file_types=["video/mp4", "video/quicktime"],
            description="Upload MP4 or MOV files to process"
        ),
        gr.Slider(
            minimum=1.0,
            maximum=5.0,
            value=2.5,
            step=0.5,
            label="Target Duration (seconds)",
            info="Length of each video segment"
        )
    ],
    outputs=gr.File(
        label="Download Processed Videos",
        file_count="single",
        type="file"
    ),
    title="Mochi-1 Video Preprocessor",
    description="""
    This tool helps prepare videos for Mochi-1 model training by:
    - Splitting videos into segments of specified duration
    - Standardizing resolution to 848x480
    - Converting to 30fps
    - Creating caption placeholder files
    """,
    article="""
    ## Processing Details
    
    Your videos will be:
    1. Split into segments of the specified duration
    2. Resized to 848x480 resolution
    3. Converted to 30fps
    4. Stripped of audio (not needed for training)
    
    For each video segment, you'll get:
    - A processed MP4 file
    - A corresponding .txt file for captions
    
    All files will be returned in a single ZIP archive.
    """,
    examples=[
        [["sample.mp4"], 2.5]
    ],
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", share=True)