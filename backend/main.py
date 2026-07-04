"""FastAPI entrypoint placeholder for the display project.

The first milestone is `scripts/infer_image.py`. This module is intentionally
minimal for now so the backend can be added without touching the original
research scripts.
"""


def app_status() -> dict[str, str]:
    return {"status": "backend scaffold created", "next": "implement FastAPI /api/predict"}

