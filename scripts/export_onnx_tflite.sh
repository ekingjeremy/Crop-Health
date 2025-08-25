#!/usr/bin/env bash
set -e
mkdir -p export

# Detection export
if [ -f runs/detect/train/weights/best.pt ]; then
  yolo export model=runs/detect/train/weights/best.pt format=onnx opset=12 imgsz=640
  yolo export model=runs/detect/train/weights/best.pt format=tflite imgsz=640
  mv runs/detect/train/weights/best.onnx export/detect_best.onnx || true
  mv runs/detect/train/weights/best.tflite export/detect_best.tflite || true
fi

# Classification export
if [ -f runs/classify/train/weights/best.pt ]; then
  yolo export model=runs/classify/train/weights/best.pt format=onnx opset=12 imgsz=224
  yolo export model=runs/classify/train/weights/best.pt format=tflite imgsz=224
  mv runs/classify/train/weights/best.onnx export/cls_best.onnx || true
  mv runs/classify/train/weights/best.tflite export/cls_best.tflite || true
fi

echo "Exports saved to export/"