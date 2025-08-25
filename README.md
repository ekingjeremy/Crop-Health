# Crop Health Monitoring with Computer Vision (Cassava-ready)

Production-style repo for **leaf-level crop diagnosis** (YOLOv8 detection + classification) and a **Streamlit** app that can run from GitHub + Streamlit Cloud. Includes a **Sentinel-2 NDVI** notebook for field-scale stress.

> Created: 2025-08-25

## Highlights
- Streamlit app entry: `streamlit_app.py` (Cloud-friendly).
- Cassava-focused class list and dataset YAMLs.
- Training scripts for detection and classification.
- Export helpers (ONNX/TFLite).
- Sentinel-2 NDVI example (`notebooks/sentinel2_ndvi.ipynb`).

## Quick Start (local)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# Train detection
bash scripts/train_detect.sh

# Train classification
bash scripts/train_classify.sh

# Run app
streamlit run streamlit_app.py
```

## Deploy on Streamlit Cloud
1. Push this folder to GitHub.
2. In Streamlit Cloud, click **New app** → pick the repo → set **Main file**: `streamlit_app.py`.
3. If you will use Sentinel Hub, add your credentials in **Secrets** as:
```toml
# (Streamlit Cloud -> App -> Settings -> Secrets)
SENTINELHUB_INSTANCE_ID="your-instance-id"
SENTINELHUB_CLIENT_ID="your-client-id"
SENTINELHUB_CLIENT_SECRET="your-client-secret"
```
4. Place your trained weights in `/weights`:
   - `detect_best.pt`
   - `cls_best.pt`
   (Or load from cloud storage/HuggingFace in your fork).

## Data layout
```
data/leaf_images/train/<class>/*.jpg
data/leaf_images/val/<class>/*.jpg

data/field_images/train/images/*.jpg   # detection images
data/field_images/train/labels/*.txt   # YOLO labels
data/field_images/val/images/*.jpg
data/field_images/val/labels/*.txt
```

## Notes
- **Generalization:** Fine-tune with your own field photos. Include look-alikes as hard negatives.
- **Active learning:** Low-confidence crops are saved to `data/active_learning/` by the app.
- **Licensing:** Check dataset licenses (PlantVillage/PlantDoc/Cassava Kaggle) before redistribution.