#!/usr/bin/env bash
set -e
yolo classify train model=yolov8n-cls.pt data=data/leaf_images epochs=50 imgsz=224 batch=64 project=runs/classify name=train