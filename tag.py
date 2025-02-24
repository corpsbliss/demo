import re

def extract_project_tags(log_file):
    project_tags = []
    pattern = r'PROJECT_TAG = (\S+)'

    with open(log_file, 'r') as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                project_tags.append(match.group(1))

    return project_tags

# Example usage
log_file_path = "your_log_file.log"  # Replace with your actual log file path
tags = extract_project_tags(log_file_path)
print(tags)