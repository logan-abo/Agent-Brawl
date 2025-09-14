!pip install ipyevents
!jupyter nbextension enable --py widgetsnbextension

from google.colab import drive
import cv2
import random
import os
import uuid

drive.mount('/content/drive')
video_path = "/content/drive/MyDrive/ML/PURE_GUS.mp4"

def extract_random_frames_fast(video_path, num_frames):
    # Use existing PURE_DATA folder in same directory as video
    parent_dir = os.path.dirname(video_path)
    output_dir = os.path.join(parent_dir, "PURE_DATA")

    if not os.path.exists(output_dir):
        raise FileNotFoundError(f"{output_dir} does not exist. Please create it first.")

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if num_frames > total_frames:
        raise ValueError("Requested more frames than available in video.")

    frame_indices = sorted(random.sample(range(total_frames), num_frames))

    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            filename = os.path.join(output_dir, f"{uuid.uuid4().hex}.jpg")
            cv2.imwrite(filename, frame)

    cap.release()
    print(f"Saved {len(frame_indices)} frames to '{output_dir}'")
