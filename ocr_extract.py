import os
import json
import torch
import easyocr
from tkinter import Tk, filedialog, messagebox
from tqdm import tqdm  # ← progress bar

# Initialize Tkinter (for file dialog only)
root = Tk()
root.withdraw()
root.update()

# Select images
image_paths = filedialog.askopenfilenames(
    title="Select Images",
    filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
)

if not image_paths:
    messagebox.showwarning("No Selection", "No images selected.")
    exit()

# Setup EasyOCR with GPU if available
use_gpu = torch.cuda.is_available()
reader = easyocr.Reader(['en'], gpu=use_gpu)

# OCR processing with progress bar
ocr_data = []
print(f"🔍 Starting OCR on {len(image_paths)} images...\n")
for path in tqdm(image_paths, desc="Processing", unit="image"):
    try:
        result = reader.readtext(path, detail=0)
        text = ' '.join(result)
        ocr_data.append({
            'image_path': path,
            'ocr_text': text
        })
    except Exception as e:
        print(f"⚠️ Error processing {path}: {e}")

# Save to JSON
with open('ocr_data.json', 'w', encoding='utf-8') as f:
    json.dump(ocr_data, f, indent=4, ensure_ascii=False)

print("\n✅ OCR extraction completed. Data saved to 'ocr_data.json'.")
root.destroy()
