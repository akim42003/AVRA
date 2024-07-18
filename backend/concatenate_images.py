from PIL import Image
import os
import sys
from db.db_utils import get_spectrogram_segments
import re

def check_files():
    folders = ['./marked_spectrogram', '../frontend/src/spectrogram']
    for folder in folders:
        if not os.path.exists(folder):
            print(f"Creating missing folder: {folder}")
            os.makedirs(folder)
        current_files = os.listdir(folder)
        if current_files:
            print(f"Clearing folder: {folder}")
            for item in current_files:
                item_path = os.path.join(folder, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)

def concatenate_images(start, end, stop):
    if int(stop) == 1:
        check_files()
        return

    print(f"Concatenating images from {start} to {end}")
    image_dir = './split_spectrograms'

    base_idx = float(start) // 3
    base_len = ((float(end) - float(start)) // 3) + 1
    db_data = get_spectrogram_segments(base_idx, (base_idx + base_len))
    print(db_data)
    base_metadata = db_data[0][0]
    num_images = len(db_data)

    if not os.path.exists(image_dir):
        print(f"Error: The directory {image_dir} does not exist.")
        return

    file_list = os.listdir(image_dir)

    def natural_sort_key(s):
        """Sort helper function to extract numbers from strings."""
        return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

    sorted_files = sorted(file_list, key=natural_sort_key)
    specified_files = sorted_files[base_metadata:(base_metadata + num_images)]
    print(specified_files)

    images = [Image.open(os.path.join(image_dir, f)) for f in specified_files]

    height = max(img.height for img in images)
    total_width = sum(img.width for img in images)

    concatenated_image = Image.new('RGB', (total_width, height))

    x_offset = 0
    for img in images:
        concatenated_image.paste(img, (x_offset, 0))
        x_offset += img.width

    check_files()
    print('Files checked')
    concatenated_image.save('./marked_spectrogram/concatenated_image.png')

if __name__ == "__main__":
    start = sys.argv[1]
    end = sys.argv[2]
    stop = sys.argv[3]
    concatenate_images(start, end, stop)
