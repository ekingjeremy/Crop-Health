# Detection Labels (YOLO format)
For each image `image.jpg`, create `image.txt` with lines:
class_id x_center y_center width height  (all normalized [0,1])

Example (single 'leaf' class -> 0):
0 0.512 0.433 0.220 0.180