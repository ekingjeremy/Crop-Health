# Sentinel-2 NDVI Example (convert to .ipynb if you prefer)
import os
import numpy as np
import matplotlib.pyplot as plt
from sentinelhub import SHConfig, SentinelHubRequest, DataCollection, bbox_to_dimensions, BBox
import os

INSTANCE_ID = os.getenv("SENTINELHUB_INSTANCE_ID")
CLIENT_ID = os.getenv("SENTINELHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("SENTINELHUB_CLIENT_SECRET")

config = SHConfig()
if INSTANCE_ID: config.instance_id = INSTANCE_ID
if CLIENT_ID: config.sh_client_id = CLIENT_ID
if CLIENT_SECRET: config.sh_client_secret = CLIENT_SECRET

# Example: small bbox in Nigeria (change to your farm coords)
bbox = BBox(bbox=[7.45, 9.25, 7.47, 9.27], crs="EPSG:4326")
resolution = 10
dims = bbox_to_dimensions(bbox, resolution=resolution)

evalscript = """
//VERSION=3
function setup() {
  return { input: ["B08", "B04"], output: { bands: 1, sampleType: "AUTO" } };
}
function evaluatePixel(s) {
  let ndvi = index(s.B08, s.B04);
  return [ndvi];
}
"""

request = SentinelHubRequest(
    data_folder=".",
    evalscript=evalscript,
    input_data=[SentinelHubRequest.input_data(data_collection=DataCollection.SENTINEL2_L2A)],
    responses=[SentinelHubRequest.output_response("default", "TIFF")],
    bbox=bbox,
    size=dims,
    config=config
)

ndvi = request.get_data()[0].squeeze()
plt.imshow(ndvi)
plt.title("NDVI")
plt.colorbar()
plt.show()