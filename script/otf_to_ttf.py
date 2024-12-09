import os
import subprocess

input_folder = os.getcwd()

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
                os.remove(otf_path)
            except subprocess.CalledProcessError as e:
                print(f"Error converting {otf_path}: {e}")
            except Exception as e:
                print(f"Error processing {otf_path}: {e}")
