import io
import os

from PIL import Image


def check_image_for_error(image_src_data):
    try:
        with Image.open(image_src_data) as img:
            img.convert("RGB")
        return False
    except Exception as e:
        print(f"Error processing image: {e}")
        return True


for root, _, files in os.walk(os.getcwd()):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(root, file)
            with open(image_path, 'rb') as image_file:
                image_data = io.BytesIO(image_file.read())
                if check_image_for_error(image_data):
                    print(f"Found problem in {image_path}")
