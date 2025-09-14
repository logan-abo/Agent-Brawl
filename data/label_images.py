import os
import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from PIL import ImageOps

# === CONFIG ===
image_dir = r"C:\Users\fabou\OneDrive\Desktop\Everything\Machine Learning\BrawlStars\PURE_DATA_FLIP"  # Replace this with your folder
json_path = os.path.join(os.path.dirname(image_dir), "labels.json")
resize_to = (800, 800)  # Display size (original coordinates will be scaled back)

# === LOAD EXISTING LABELS ===
if os.path.exists(json_path):
    with open(json_path, "r") as f:
        labels = json.load(f)
else:
    labels = {}

# === GET IMAGES TO LABEL ===
all_images = [f for f in os.listdir(image_dir) if f.endswith(".jpg")]
images_to_label = [f for f in all_images if f not in labels]
current_index = 0

# === INIT TK ===
root = tk.Tk()
root.title("Image Click Labeling")

canvas = tk.Canvas(root, width=resize_to[0], height=resize_to[1])
canvas.pack()

status_label = tk.Label(root, text="")
status_label.pack()

def save_json():
    with open(json_path, "w") as f:
        json.dump(labels, f, indent=2)

def show_image():
    global photo, current_image_path, scale_x, scale_y, current_fname

    if current_index >= len(images_to_label):
        messagebox.showinfo("Done", "All images labeled or skipped.")
        root.destroy()
        return

    fname = images_to_label[current_index]
    current_image_path = os.path.join(image_dir, fname)
    img = Image.open(current_image_path)

    # 🔄 Rotate 90° CCW
    img = img.rotate(90, expand=True)

    # Get new dimensions
    orig_width, orig_height = img.size
    if orig_width >= orig_height:
        new_width = 800
        new_height = int(orig_height * (800 / orig_width))
    else:
        new_height = 800
        new_width = int(orig_width * (800 / orig_height))

    # Resize proportionally
    img_resized = img.resize((new_width, new_height))

    # Track scale
    scale_x = orig_width / new_width
    scale_y = orig_height / new_height
    current_fname = fname

    # Update canvas size
    canvas.config(width=new_width, height=new_height)

    photo = ImageTk.PhotoImage(img_resized)
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)
    status_label.config(text=f"{fname} — Click to label or press Skip")
    
def on_click(event):
    global current_index

    x_click = event.x
    y_click = event.y

    x = int(x_click * scale_x)
    y = int(y_click * scale_y)

    # ✅ Normalize using original image dimensions
    orig_img = Image.open(current_image_path).rotate(90, expand=True)
    norm_x = x / orig_img.width
    norm_y = y / orig_img.height

    fname = images_to_label[current_index]
    labels[fname] = [round(norm_x, 6), round(norm_y, 6)]  # rounded for readability
    save_json()

    current_index += 1
    show_image()

def skip_image():
    global current_index
    fname = images_to_label[current_index]
    try:
        os.remove(os.path.join(image_dir, fname))
    except:
        messagebox.showerror("Error", f"Failed to delete {fname}")
    current_index += 1
    show_image()

# === BINDINGS & BUTTONS ===
canvas.bind("<Button-1>", on_click)

skip_button = tk.Button(root, text="Skip (Delete Image)", command=skip_image, bg="red", fg="white")
skip_button.pack(pady=10)

# === START ===
show_image()
root.mainloop()
