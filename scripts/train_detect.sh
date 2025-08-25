#!/usr/bin/env bash
set -e
yolo detect train model=yolov8n.pt data=configs/dataset_leaf_detection.yaml epochs=100 imgsz=640 batch=32 project=runs/detect name=train