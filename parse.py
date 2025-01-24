# Define the file path
log_file_path = "path/to/your/logfile.txt"

# Initialize variables
version_major = None
project_tag = None

# Read the log file
with open(log_file_path, "r") as file:
    for line in file:
        # Extract Version_major
        if "Version_major" in line:
            version_major = line.split("=")[1].strip()
        # Extract project_tag
        if "project_tag" in line:
            project_tag = line.split("=")[1].strip()

# Print the extracted values
print(f"Version_major: {version_major}")
print(f"Project_tag: {project_tag}")