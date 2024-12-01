# Complete Guide to Fine-tuning the Mochi-1 Video Model

## Introduction
This guide will walk you through the process of fine-tuning the Mochi-1 video model. There are two possible approaches:
1. Full model fine-tuning (requires multiple GPUs)
2. LoRA fine-tuning (works with a single GPU)

## System Requirements

### Hardware Requirements
- **Single GPU Setup**
  - 1 NVIDIA H100 GPU
  - 80GB VRAM (Video Memory)
  - Note: Other GPU models are not supported due to memory requirements

- **Multi-GPU Setup**
  - 8 NVIDIA H100 GPUs
  - Total of 640GB VRAM across all GPUs

### Video Length Limitations
- Single GPU: Maximum 85 frames (approximately 2.4 seconds at 30 FPS)
- Multi-GPU: Maximum 163 frames (approximately 5.4 seconds at 30 FPS)

## Detailed Step-by-Step Guide

### Step 1: Dataset Preparation

#### 1.1 Video Collection
1. Gather your video files
   - Supported formats: MP4 and MOV only
   - Make sure your videos are high quality and well-lit
   - Create a dedicated folder for your videos (e.g., `my_video_folder`)

#### 1.2 Video Processing
1. Open your terminal/command prompt
2. Navigate to your project directory
3. Run the trim and crop script:
```bash
./demos/fine_tuner/trim_and_crop.py my_video_folder -d 2.5
```
This script will:
- Automatically resize all videos to 480p resolution
- Trim each video to the first 2.5 seconds
- Process all videos in your specified folder

#### 1.3 Caption Creation
1. For each video in your dataset, create a matching text file:
   - If your video is named `video.mp4`, create `video.txt`
   - The text file should be in the same folder as the video
   - Write your caption describing the video in the text file

2. Generate caption embeddings:
```bash
python3 ./demos/fine_tuner/embed_captions.py my_video_folder
```
This creates `.embed.pt` files for each caption

#### 1.4 Video Embedding Generation
1. Run the video embedding script:
```bash
python3 ./demos/fine_tuner/embed_videos.py my_video_folder <encoder_path> <decoder_path> --num_gpus 1 --shape "85x480x848"
```
- Replace `<encoder_path>` with the path to your encoder model
- Replace `<decoder_path>` with the path to your decoder model (optional)
- The script will create `.embed.pt` files for your videos

Note: Including the decoder_path is recommended for beginners as it allows you to verify your embeddings by reconstructing sample videos.

### Step 2: Configuration Setup

1. Create your configuration file:
```bash
cp configs/lora.yaml.example configs/your_lora_config.yaml
```

2. Edit your configuration file:
   - Open `configs/your_lora_config.yaml` in a text editor
   - Modify the parameters according to your needs
   - Save the changes

### Step 3: Fine-tuning

#### For Single GPU (LoRA Fine-tuning)
1. Start the fine-tuning process:
```bash
./demos/fine_tuner/run.bash -c ./demos/fine_tuner/configs/your_lora_config.yaml -n 1
```
- The `-n 1` parameter specifies using 1 GPU
- Monitor the training progress in your terminal

### Step 4: Running Inference

1. After training completes, run inference:
```bash
python3 ./demos/cli.py --model_dir "<path_to_downloaded_directory>" --lora_path "<path_to_lora>"
```
Replace:
- `<path_to_downloaded_directory>` with your model directory path
- `<path_to_lora>` with the path to your trained LoRA weights

## Important Limitations

1. LoRA Restrictions:
   - Only works with single GPU setups
   - Cannot be distributed across multiple GPUs
   - Inference also limited to single GPU

2. Video Length Restrictions:
   - Single GPU: Maximum 85 frames
   - Multi-GPU: Maximum 163 frames

3. Technical Notes:
   - LoRA fine-tuning only updates query and value projection matrices
   - Make sure to stay within frame limits for your setup

## Troubleshooting Tips

1. If videos aren't processing:
   - Check file formats (only MP4 and MOV supported)
   - Verify video lengths are within limits
   - Ensure sufficient disk space

2. If embedding fails:
   - Verify GPU has enough memory
   - Check path specifications are correct
   - Ensure videos were properly preprocessed

3. If training crashes:
   - Monitor GPU memory usage
   - Verify configuration file settings
   - Check system meets minimum requirements
