import os
from PIL import Image, UnidentifiedImageError

from tools import for_print_path

if __name__ == "__main__":
    # 使用 os.walk 遍历所有子文件夹和文件
    for root, _, filenames in os.walk(os.getcwd()):
        for filename in filenames:
            if filename.lower().startswith("cover"):  # 检查是否以 "cover" 开头（不区分大小写）
                file_path = os.path.join(root, filename)

                try:
                    # 尝试使用 PIL 打开文件
                    with Image.open(file_path) as img:
                        # 获取文件格式并转为小写
                        ext = img.format.lower()

                        # 构造新文件名
                        new_file_name = f"cover.{ext}"
                        new_file_path = os.path.join(root, new_file_name)

                        # 如果文件名已经正确，跳过重命名
                        if file_path == new_file_path:
                            continue

                        # 重命名文件
                        os.rename(file_path, new_file_path)
                        print(f"重命名: {for_print_path(os.getcwd(), file_path)} -> {new_file_name}")
                except UnidentifiedImageError:
                    pass
