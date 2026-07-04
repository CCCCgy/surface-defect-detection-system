"""Detector wrapper placeholder.

Planned role:
- load the CE7 YOLO weight once at backend startup
- expose a `predict_image()` function for FastAPI
- return JSON-serializable detections and visualization paths
"""

from pathlib import Path
import os


DEFAULT_WEIGHTS = Path(os.environ.get("CERAMIC_YOLO_WEIGHTS", "path/to/your/local/best.pt"))
CLASS_NAMES = ("CK", "DS", "GS", "SS", "EC", "AC", "PH")
