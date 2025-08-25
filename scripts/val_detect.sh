#!/usr/bin/env bash
set -e
yolo detect val model=runs/detect/train/weights/best.pt data=configs/dataset_leaf_detection.yaml