import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import os

def load_model(path):
    if os.path.exists(path):
        try:
            return YOLO(path)
        except Exception as e:
            st.error(f"Failed to load model: {e}")
    return None

def run_inference(det_model, cls_model, image, conf_thresh=0.25):
    det_res = det_model.predict(source=np.array(image), conf=conf_thresh, verbose=False)[0]
    outputs = []
    if det_res.boxes is None or len(det_res.boxes) == 0:
        return outputs

    for b in det_res.boxes:
        x1, y1, x2, y2 = map(int, b.xyxy[0])
        crop = image.crop((x1, y1, x2, y2)).resize((224, 224))
        pred = {"crop": crop, "prediction": None, "confidence": None}
        if cls_model is not None:
            cls_res = cls_model.predict(source=np.array(crop), verbose=False)[0]
            names = cls_res.names
            top1 = int(cls_res.probs.top1)
            conf = float(cls_res.probs.top1conf)
            pred["prediction"] = names[top1]
            pred["confidence"] = conf
        outputs.append(pred)
    return outputs

def main():
    st.set_page_config(page_title="Crop Health Monitor", layout="centered")
    st.title("🌿 Crop Health Monitor — Cassava Edition")

    st.info("Upload a field image. The app detects leaf regions and classifies health status. "
            "Place your trained models in the 'weights/' folder as 'detect_best.pt' and 'cls_best.pt'.")

    DETECT_WEIGHTS = os.path.join("weights", "detect_best.pt")
    CLASSIFY_WEIGHTS = os.path.join("weights", "cls_best.pt")

    det_model = load_model(DETECT_WEIGHTS)
    cls_model = load_model(CLASSIFY_WEIGHTS)

    if det_model is None:
        st.warning("No detection model found at weights/detect_best.pt — run training or upload weights.")

    img_file = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])
    conf_thresh = st.slider("Detection confidence", 0.1, 0.9, 0.25, 0.05)

    if img_file and det_model is not None:
        image = Image.open(img_file).convert("RGB")
        st.image(image, caption="Original", use_column_width=True)

        results = run_inference(det_model, cls_model, image, conf_thresh=conf_thresh)
        if not results:
            st.warning("No leaves detected. Try lowering confidence or upload a closer photo.")
        else:
            for idx, r in enumerate(results, start=1):
                st.subheader(f"Leaf {idx}")
                st.image(r["crop"], width=256)
                if r["prediction"]:
                    st.success(f"Prediction: **{r['prediction']}** ({r['confidence']:.2f})")
                    if r["confidence"] < 0.65:
                        os.makedirs("data/active_learning", exist_ok=True)
                        save_path = os.path.join("data/active_learning", f"lowconf_{idx}.png")
                        r["crop"].save(save_path)
                        st.caption(f"Saved low-confidence crop → {save_path}")
                else:
                    st.info("Upload classification weights to enable disease identification.")

if __name__ == "__main__":
    main()