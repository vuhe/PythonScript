import argparse
import os
import re
import subprocess
import shutil


def run_assfonts(input_file, force=False):
    # Extract base name and potential language tag
    base_name = os.path.basename(input_file)
    match = re.match(r'(.+?)(\.(\w+))?\.ass$', base_name)

    if not match:
        print(f"Skipping: '{input_file}' is not a valid .ass file.")
        return

    title, _, lang_tag = match.groups()
    lang_suffix = f".{lang_tag}" if lang_tag else ""
    output_file = f"{title}.assfonts{lang_suffix}.forced.ass"
    extra_folder = f"{title}{lang_suffix}_subsetted"

    # Check if the output file already exists
    if os.path.isfile(output_file) and not force:
        print(f"Skipping: '{output_file}' already exists. Use -f or --force to overwrite.")
        return

    # Run the `assfonts` command
    command = ["assfonts", "-i", input_file]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    generated_output = f"{title}{lang_suffix}.assfonts.ass"

    # Check for `[WARN]` in output
    if "[WARN]" in stdout or "[WARN]" in stderr:
        print(f"[WARN] encountered while processing '{input_file}'. Stopping.")
        print(stdout or stderr)
        if os.path.isfile(generated_output):
            os.remove(generated_output)
        exit(-1)

    # Check if the expected output file exists
    if os.path.isfile(generated_output):
        os.rename(generated_output, output_file)
        print(f"Successfully processed and renamed to: {output_file}")
    else:
        print(f"Error: Expected output file '{generated_output}' not found.")

    # Check for and delete the extra folder
    if os.path.isdir(extra_folder):
        try:
            shutil.rmtree(extra_folder)
            print(f"Deleted folder: {extra_folder}")
        except Exception as e:
            print(f"Error deleting folder '{extra_folder}': {e}")


parser = argparse.ArgumentParser(description="Batch process ASS files in a folder with assfonts.")
parser.add_argument("-f", "--force", action="store_true", help="Force processing even if the output file exists")

args = parser.parse_args()
input_folder = os.getcwd()

for file in os.listdir(input_folder):
    if file.lower().endswith(".ass"):
        ass_path = os.path.join(input_folder, file)
        run_assfonts(ass_path, args.force)
