"""
Local Video Captioner
A tool for generating captions for short videos using LLaVA model locally.
"""

from pathlib import Path
import os

# Version information
__version__ = '1.0.0'
__author__ = 'Your Name'
__license__ = 'MIT'

# Import main functionality
from .video_captioner import LocalVideoCaptioner
from .preprocess_videos import preprocess_videos

# Package level constants
DEFAULT_MODEL_DIR = Path(os.path.dirname(os.path.dirname(__file__))) / 'models'
DEFAULT_MODEL_NAME = 'llava-v1.5-7b-Q4_K.gguf'
DEFAULT_MODEL_PATH = DEFAULT_MODEL_DIR / DEFAULT_MODEL_NAME

# Video preprocessing constants
DEFAULT_VIDEO_DURATION = 2.5  # seconds
DEFAULT_VIDEO_WIDTH = 848    # pixels
DEFAULT_VIDEO_HEIGHT = 480   # pixels
DEFAULT_VIDEO_FPS = 30       # frames per second

# Utility functions for package-level use
def get_default_model_path():
    """Returns the default path where the LLaVA model should be placed."""
    return DEFAULT_MODEL_PATH

def verify_model_exists():
    """Check if the model file exists in the expected location."""
    return DEFAULT_MODEL_PATH.exists()

def get_version():
    """Returns the current version of the package."""
    return __version__

def get_video_requirements():
    """Returns the default video processing requirements."""
    return {
        'duration': DEFAULT_VIDEO_DURATION,
        'width': DEFAULT_VIDEO_WIDTH,
        'height': DEFAULT_VIDEO_HEIGHT,
        'fps': DEFAULT_VIDEO_FPS
    }

# Make key classes and functions available at package level
__all__ = [
    'LocalVideoCaptioner',
    'preprocess_videos',
    'get_default_model_path',
    'verify_model_exists',
    'get_version',
    'get_video_requirements',
]