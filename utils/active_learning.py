import os
from PIL import Image

def save_low_confidence(image: Image.Image, path: str, threshold: float, prob: float):
    if prob < threshold:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        image.save(path)