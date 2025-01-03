import click
from pathlib import Path
import shutil
import sys
from moviepy.editor import VideoFileClip
from tqdm import tqdm
import math

def validate_system_requirements():
    """Check if required packages are available."""
    try:
        import moviepy
        import tqdm
    except ImportError:
        print("Error: Required packages not found. Please run:")
        print("pip install moviepy tqdm")
        sys.exit(1)

@click.command()
@click.argument("input_folder", type=click.Path(exists=True, dir_okay=True))
@click.argument("output_folder", type=click.Path(dir_okay=True))
@click.option("--duration", "-d", type=float, default=2.5, 
              help="Target duration in seconds (default: 2.5)")
@click.option("--width", "-w", type=int, default=848,
              help="Target width in pixels (default: 848)")
@click.option("--height", "-h", type=int, default=480,
              help="Target height in pixels (default: 480)")
@click.option("--fps", "-f", type=int, default=30,
              help="Target framerate (default: 30)")
def preprocess_videos(input_folder, output_folder, duration, width, height, fps):
    """
    Preprocess videos for Mochi-1 training by standardizing duration and resolution.
    Splits longer videos into multiple segments of specified duration.
    
    INPUT_FOLDER: Path to folder containing input videos
    OUTPUT_FOLDER: Path where processed videos will be saved
    """
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    # Find all video files (case-insensitive)
    video_files = []
    for ext in ['.mp4', '.mov']:
        video_files.extend(list(input_path.rglob(f'*{ext}')) + 
                         list(input_path.rglob(f'*{ext.upper()}')))

    if not video_files:
        print(f"No video files found in {input_folder}")
        return

    print(f"\nProcessing {len(video_files)} videos...")
    print(f"Target format: {width}x{height}, {duration}s, {fps}fps")
    
    for file_path in tqdm(video_files, desc="Processing videos"):
        try:
            # Load video
            video = VideoFileClip(str(file_path))

            # Skip if video is too short
            if video.duration < duration:
                print(f"\nSkipping {file_path.name}: too short ({video.duration:.1f}s < {duration}s)")
                continue

            # Calculate number of segments
            num_segments = math.floor(video.duration / duration)
            print(f"\nSplitting {file_path.name} into {num_segments} segments")

            # Process each segment
            for segment_idx in range(num_segments):
                # Calculate segment time range
                start_time = segment_idx * duration
                end_time = start_time + duration

                # Setup output paths for this segment
                segment_name = f"{file_path.stem}_segment{segment_idx+1}.mp4"
                output_file = output_path / segment_name
                output_file.parent.mkdir(parents=True, exist_ok=True)

                # Extract segment
                segment = video.subclip(start_time, end_time)

                # Calculate dimensions to maintain aspect ratio
                target_ratio = width / height
                current_ratio = video.w / video.h

                if current_ratio > target_ratio:
                    # Video is wider - crop width
                    new_width = int(video.h * target_ratio)
                    x1 = (video.w - new_width) // 2
                    final = segment.crop(x1=x1, width=new_width)
                else:
                    # Video is taller - crop height
                    new_height = int(video.w / target_ratio)
                    y1 = (video.h - new_height) // 2
                    final = segment.crop(y1=y1, height=new_height)

                # Resize to target resolution
                final = final.resize((width, height))
                final = final.set_fps(fps)

                # Configure output settings
                output_params = {
                    "codec": "libx264",
                    "audio": False,
                    "preset": "medium",
                    "bitrate": "5000k",
                }

                # Handle caption file
                txt_path = file_path.with_suffix('.txt')
                if txt_path.exists():
                    # Create segment-specific caption file
                    output_txt = output_path / f"{file_path.stem}_segment{segment_idx+1}.txt"
                    shutil.copy(txt_path, output_txt)
                else:
                    print(f"\nWarning: No caption file found for {file_path.name}")
                    output_txt = output_path / f"{file_path.stem}_segment{segment_idx+1}.txt"
                    output_txt.touch()  # Create empty file

                # Save processed segment
                final.write_videofile(str(output_file), **output_params)

                # Cleanup segment
                segment.close()
                final.close()

            # Cleanup original video
            video.close()

        except Exception as e:
            print(f"\nError processing {file_path.name}: {str(e)}")
            continue

    print("\nProcessing complete!")
    print(f"Processed video segments saved to: {output_path}")

if __name__ == "__main__":
    try:
        validate_system_requirements()
        preprocess_videos()
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)