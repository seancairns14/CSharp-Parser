import os
import shutil


def find_and_copy_dll(source_dir, destination_dir):
    # Check if the source directory exists
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return

    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Traverse through the source directory
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.dll'):  # Check for DLL files
                dll_path = os.path.join(root, file)
                print(f"Copying {dll_path} to {destination_dir}")
                shutil.copy(dll_path, destination_dir)


# Replace these paths with your source and destination directories
source_directory = 'C:\Program Files (x86)\Steam\steamapps\common\VRising'
destination_directory = './dll'

find_and_copy_dll(source_directory, destination_directory)
