import tarfile
import os

# Path to your .tar.gz file
file_path = "/path/to/your/file.tar.gz"

# Get the file name without extension
folder_name = os.path.splitext(os.path.basename(file_path))[0]
folder_name = os.path.splitext(folder_name)[0]  # In case of double extensions like .tar.gz

# Create a folder with the same name as the file
output_folder = os.path.join(os.path.dirname(file_path), folder_name)

# Create the folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Extract the tar.gz file into the created folder
with tarfile.open(file_path, "r:gz") as tar:
    tar.extractall(path=output_folder)

print(f"File extracted to: {output_folder}")