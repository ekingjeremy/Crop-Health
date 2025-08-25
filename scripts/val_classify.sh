#!/usr/bin/env bash
set -e
yolo classify val model=runs/classify/train/weights/best.pt data=data/leaf_images