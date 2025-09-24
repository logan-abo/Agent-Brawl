import os
import json
from PIL import Image

def rotate_images_and_adjust_labels(image_folder, labels_path):
    # Load labels if available
    if os.path.exists(labels_path):
        with open(labels_path, 'r') as f:
            labels = json.load(f)
    else:
        labels = {}

    updated_labels = {}

    for fname in os.listdir(image_folder):
        if not fname.lower().endswith(('.jpg', '.png', '.jpeg')):
            continue

        img_path = os.path.join(image_folder, fname)

        # Rotate the image 180 degrees
        img = Image.open(img_path)
        img_rotated = img.rotate(180, expand=True)
        img_rotated.save(img_path)  # Overwrite the original file

        # Update label if it's in labels.json
        if fname in labels:
            x, y = labels[fname]
            new_x = 1.0 - x
            new_y = 1.0 - y
            updated_labels[fname] = [round(new_x, 6), round(new_y, 6)]

    # Save updated labels
    with open(labels_path, 'w') as f:
        json.dump(updated_labels, f, indent=2)

rotate_images_and_adjust_labels(
    r"C:\Users\fabou\OneDrive\Desktop\Everything\Machine Learning\BrawlStars\PURE_DATA_FLIP",
    r"C:\Users\fabou\OneDrive\Desktop\Everything\Machine Learning\BrawlStars\labels.json"
)
