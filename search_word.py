import os
import json
import shutil
from tkinter import Tk, simpledialog, messagebox

# Initialize Tkinter
root = Tk()
root.withdraw()
root.update()

# Ask for word to search
search_word = simpledialog.askstring("Search Word", "Enter the word to search for:")
root.update()

if not search_word:
    messagebox.showwarning("Input Missing", "No search word entered.")
    exit()

# Load OCR data
if not os.path.exists("ocr_data.json"):
    messagebox.showerror("Missing File", "'ocr_data.json' not found. Run Part 1 first.")
    exit()

with open("ocr_data.json", "r", encoding="utf-8") as f:
    ocr_data = json.load(f)

# Create output folder
output_folder = "results"
os.makedirs(output_folder, exist_ok=True)

# Search and copy
matched_images = []
for entry in ocr_data:
    if search_word.lower() in entry['ocr_text'].lower():
        try:
            shutil.copy(entry['image_path'], output_folder)
            matched_images.append(os.path.basename(entry['image_path']))
        except Exception as e:
            print(f"⚠️ Error copying file: {e}")

# Show result
if matched_images:
    messagebox.showinfo("Done", f"✅ Found '{search_word}' in {len(matched_images)} image(s).\nCopied to 'results/' folder.")
else:
    messagebox.showinfo("No Match", f"❌ No matches found for '{search_word}'.")

root.destroy()
