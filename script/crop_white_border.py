from PIL import Image
import os
import numpy as np


def get_min_white_border(image_files):
    min_left, min_right = float('inf'), float('inf')

    for file in image_files:
        img = Image.open(file).convert("RGB")
        img_array = np.array(img)

        # 计算每列的非白色像素（假设纯白为 255, 255, 255）
        non_white = np.any(img_array != [255, 255, 255], axis=-1)
        cols = np.any(non_white, axis=0)

        # 找到最左和最右的非白色列
        left, right = np.argmax(cols), len(cols) - np.argmax(cols[::-1])

        min_left = min(min_left, left)
        min_right = min(min_right, len(cols) - right)

    return min_left, min_right


def crop_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder)
                   if f.lower().endswith(('png', 'jpg', 'jpeg'))]

    if not image_files:
        print("未找到图片文件")
        return

    min_left, min_right = get_min_white_border(image_files)

    for file in image_files:
        img = Image.open(file)
        width, height = img.size
        cropped = img.crop((min_left, 0, width - min_right, height))
        output_path = os.path.join(output_folder, os.path.basename(file))
        cropped.save(output_path, "PNG")

    print(f"所有图片已裁剪并保存到 {output_folder}")


if __name__ == "__main__":
    cwd = os.getcwd()  # 当前文件夹
    output = os.path.join(cwd, "output")
    crop_images(cwd, output)
