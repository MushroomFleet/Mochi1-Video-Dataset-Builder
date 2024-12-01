"""
Video Preprocessor for Mochi-1 Training
A tool for preprocessing videos into the format required by Mochi-1 model training.
"""

from pathlib import Path
import os

# Version information
__version__ = '1.0.0'
__author__ = 'Your Name'
__license__ = 'MIT'

# Import main functionality
from .preprocess_videos import preprocess_videos

# Package level constants
DEFAULT_VIDEO_DURATION = 2.5  # seconds
DEFAULT_VIDEO_WIDTH = 848    # pixels
DEFAULT_VIDEO_HEIGHT = 480   # pixels
DEFAULT_VIDEO_FPS = 30       # frames per second

# Utility functions for package-level use
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
    'preprocess_videos',
    'get_version',
    'get_video_requirements',
]