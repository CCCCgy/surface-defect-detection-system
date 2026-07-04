from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import cv2


PROJECT_DIR = Path(__file__).resolve().parents[1]
YOLO_SOURCE_ENV = "YOLO_SOURCE_DIR"
WEIGHTS_ENV = "CERAMIC_YOLO_WEIGHTS"
DEFAULT_WEIGHTS = Path(os.environ.get(WEIGHTS_ENV, "path/to/your/local/best.pt"))
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[1] / "assets" / "demo_outputs"

CLASS_NAMES = ("CK", "DS", "GS", "SS", "EC", "AC", "PH")
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


def load_yolo_class():
    yolo_source = os.environ.get(YOLO_SOURCE_ENV)
    if yolo_source:
        yolo_source_path = Path(yolo_source).expanduser()
        if yolo_source_path.exists() and str(yolo_source_path) not in sys.path:
            sys.path.insert(0, str(yolo_source_path))

    try:
        from ultralytics import YOLO
    except ImportError as exc:
        raise ImportError(
            "Cannot import ultralytics. Install dependencies with "
            "`pip install -r requirements.txt`, or set YOLO_SOURCE_DIR to a local "
            "Ultralytics source checkout."
        ) from exc

    return YOLO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run single-image YOLO inference for CE7-DET ceramic defect detection."
    )
    parser.add_argument(
        "--weights",
        type=Path,
        default=DEFAULT_WEIGHTS,
        help=f"Local model weight path. Can also be set via {WEIGHTS_ENV}.",
    )
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--iou", type=float, default=0.60)
    parser.add_argument("--imgsz", type=int, default=800)
    return parser.parse_args()


def validate_inputs(weights: Path, source: Path) -> None:
    if not weights.exists():
        raise FileNotFoundError(f"Weights file not found: {weights}")
    if not source.exists():
        raise FileNotFoundError(f"Source image not found: {source}")
    if not source.is_file() or source.suffix.lower() not in IMAGE_SUFFIXES:
        raise ValueError(f"Source must be a single image file: {source}")


def class_name(class_id: int) -> str:
    if 0 <= class_id < len(CLASS_NAMES):
        return CLASS_NAMES[class_id]
    return str(class_id)


def detections_from_result(result: Any) -> list[dict[str, Any]]:
    if result.boxes is None or len(result.boxes) == 0:
        return []

    boxes = result.boxes
    xyxy = boxes.xyxy.detach().cpu().tolist()
    confs = boxes.conf.detach().cpu().tolist()
    class_ids = boxes.cls.detach().cpu().to(int).tolist()

    detections: list[dict[str, Any]] = []
    for box, conf, class_id in zip(xyxy, confs, class_ids):
        detections.append(
            {
                "class_id": int(class_id),
                "class_name": class_name(int(class_id)),
                "confidence": round(float(conf), 4),
                "bbox_xyxy": [round(float(value), 4) for value in box],
            }
        )
    return detections


def draw_detections(source: Path, detections: list[dict[str, Any]], output_image: Path) -> None:
    image = cv2.imread(str(source))
    if image is None:
        raise ValueError(f"Failed to read image: {source}")

    for det in detections:
        x1, y1, x2, y2 = [int(round(v)) for v in det["bbox_xyxy"]]
        label = f"{det['class_name']} {det['confidence']:.2f}"
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 200, 255), 2)
        text_y = max(20, y1 - 8)
        cv2.putText(
            image,
            label,
            (x1, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 200, 255),
            2,
            cv2.LINE_AA,
        )

    output_image.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output_image), image):
        raise RuntimeError(f"Failed to write visualization: {output_image}")


def write_json(
    output_json: Path,
    source: Path,
    weights: Path,
    output_image: Path,
    detections: list[dict[str, Any]],
    inference_time_ms: float,
    args: argparse.Namespace,
) -> None:
    payload = {
        "source_name": source.name,
        "weights_name": weights.name,
        "visualization_name": output_image.name,
        "class_names": list(CLASS_NAMES),
        "parameters": {
            "conf": args.conf,
            "iou": args.iou,
            "imgsz": args.imgsz,
        },
        "inference_time_ms": round(inference_time_ms, 2),
        "boxes": detections,
    }
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    args = parse_args()
    weights = args.weights.expanduser().resolve()
    source = args.source.resolve()
    output_dir = args.output_dir.resolve()

    validate_inputs(weights, source)

    YOLO = load_yolo_class()
    model = YOLO(str(weights))

    start = time.perf_counter()
    results = model.predict(
        source=str(source),
        imgsz=args.imgsz,
        conf=args.conf,
        iou=args.iou,
        verbose=False,
    )
    inference_time_ms = (time.perf_counter() - start) * 1000.0

    if not results:
        raise RuntimeError("YOLO returned no result object.")

    detections = detections_from_result(results[0])
    stem = source.stem
    output_image = output_dir / f"{stem}_pred.jpg"
    output_json = output_dir / f"{stem}_result.json"

    draw_detections(source, detections, output_image)
    write_json(output_json, source, weights, output_image, detections, inference_time_ms, args)

    print(f"Visualization: {output_image}")
    print(f"JSON result: {output_json}")
    print(f"Detections: {len(detections)}")
    print(f"Inference time: {inference_time_ms:.2f} ms")


if __name__ == "__main__":
    main()
