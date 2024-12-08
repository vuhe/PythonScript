import os
import shutil
import subprocess

input_folder = os.getcwd()

# Create a backup folder in the current working directory
backup_folder = os.path.join(input_folder, "backup")
os.makedirs(backup_folder, exist_ok=True)

# Traverse the input folder for .otf files
for root, _, files in os.walk(input_folder):
    for file in files:
        if file.lower().endswith(".otf"):
            otf_path = os.path.join(root, file)
            ttf_path = os.path.splitext(otf_path)[0] + ".ttf"

            # Convert the OTF to TTF
            try:
                subprocess.run(["otf2ttf", otf_path], check=True)
                print(f"Converted: {otf_path} -> {ttf_path}")

                # Backup the original OTF file
                backup_path = os.path.join(backup_folder, file)
                shutil.move(otf_path, backup_path)
                print(f"Backed up: {otf_path} -> {backup_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error converting {otf_path}: {e}")
            except Exception as e:
                print(f"Error processing {otf_path}: {e}")
