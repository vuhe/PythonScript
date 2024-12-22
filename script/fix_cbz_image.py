import os
import zipfile
import io
from PIL import Image
import subprocess

from tools import for_print_path


def convert_jpeg_to_jxl(jpeg_data):
    """
    Convert JPEG data to JXL using a subprocess for the cjxl command-line tool.
    Returns the JXL binary data.
    """
    try:
        process = subprocess.run(
            ["cjxl", "-", "-"],  # No need for -d 0 for JPEG, as cjxl defaults to lossless for JPEG
            input=jpeg_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return process.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error converting JPEG to JXL: {e.stderr.decode()}")
        return None


def convert_png_to_jxl(png_data):
    """
    Convert PNG data to JXL using a subprocess for the cjxl command-line tool.
    Returns the JXL binary data.
    """
    try:
        process = subprocess.run(
            ["cjxl", "-", "-", "-d", "0"],
            input=png_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return process.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error converting PNG to JXL: {e.stderr.decode()}")
        return None


def check_zip_file(zip_path):
    changes_made = False

    with zipfile.ZipFile(zip_path, 'r') as original_zip:
        for item in original_zip.infolist():
            if changes_made:
                break
            with original_zip.open(item.filename) as original_zip_file:
                data = original_zip_file.read()

                # Check if the file is an image
                try:
                    img = Image.open(io.BytesIO(data))
                    img.verify()  # Verify image integrity

                    # Correct suffix if necessary
                    if not item.filename.endswith(f".{img.format.lower()}"):
                        changes_made = True

                    # Convert PNG to JXL
                    if img.format == "PNG":
                        changes_made = True

                    # Convert JPEG to JXL
                    elif img.format == "JPEG":
                        changes_made = True

                except (IOError, OSError):
                    pass  # Not an image, write as is

    #	if not changes_made:
    #		print(f"Skip: {zip_path}")

    return changes_made


def process_zip_file(zip_path):
    print(f"Updating: {for_print_path(os.getcwd(), zip_path)}")
    temp_zip_path = zip_path + ".tmp"
    changes_made = False

    with zipfile.ZipFile(zip_path, 'r') as original_zip:
        with zipfile.ZipFile(temp_zip_path, 'w', compression=zipfile.ZIP_STORED) as new_zip:
            for item in original_zip.infolist():
                with original_zip.open(item.filename) as original_zip_file:
                    data = original_zip_file.read()
                    new_filename = item.filename

                    # Check if the file is an image
                    try:
                        img = Image.open(io.BytesIO(data))
                        img.verify()  # Verify image integrity

                        # Correct suffix if necessary
                        if not item.filename.endswith(f".{img.format.lower()}"):
                            new_filename = f"{os.path.splitext(item.filename)[0]}.{img.format.lower()}"
                            changes_made = True

                        # Convert PNG to JXL
                        if img.format == "PNG":
                            jxl_data = convert_png_to_jxl(data)
                            if jxl_data:
                                new_filename = f"{os.path.splitext(new_filename)[0]}.jxl"
                                new_zip.writestr(new_filename, jxl_data)
                                changes_made = True
                                continue

                        # Convert JPEG to JXL
                        elif img.format == "JPEG":
                            jxl_data = convert_jpeg_to_jxl(data)
                            if jxl_data:
                                new_filename = f"{os.path.splitext(new_filename)[0]}.jxl"
                                new_zip.writestr(new_filename, jxl_data)
                                changes_made = True
                                continue

                    except (IOError, OSError):
                        pass  # Not an image, write as is

                    # Write the original file if no changes were made
                    new_zip.writestr(new_filename, data)

    # Replace the original ZIP file only if changes were made
    if changes_made:
        os.replace(temp_zip_path, zip_path)
    else:
        os.remove(temp_zip_path)
        print(f"No changes made to: {zip_path}")


for root, _, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith(".cbz") and check_zip_file(os.path.join(root, file)):
            process_zip_file(os.path.join(root, file))
