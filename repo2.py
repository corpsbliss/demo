import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_latest_folder(base_url):
    """Find the latest folder from the given URL directory listing."""
    response = requests.get(base_url)
    if response.status_code != 200:
        raise Exception(f"Failed to access {base_url}. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    
    # Extract folder names and their links
    folders = []
    for link in links:
        href = link.get('href')
        if href and href.endswith('/'):  # Look for folder links
            folders.append(href)

    if not folders:
        raise Exception("No folders found on the server.")

    # Sort by folder names (assumes folders are named in sortable order)
    latest_folder = sorted(folders)[-1]
    print(f"Latest folder: {latest_folder}")
    return urljoin(base_url, latest_folder)

def find_specific_file(folder_url, partial_file_name):
    """Search for a file with a partial match in the folder."""
    response = requests.get(folder_url)
    if response.status_code != 200:
        raise Exception(f"Failed to access {folder_url}. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    
    # Look for a file matching the partial name
    for link in links:
        href = link.get('href')
        if href and partial_file_name in href:  # Partial match
            print(f"Found file: {href}")
            return urljoin(folder_url, href)
    
    return None

def download_file(file_url, local_dir):
    """Download the specific file."""
    response = requests.get(file_url, stream=True)

    if response.status_code == 200:
        file_name = os.path.basename(file_url)
        os.makedirs(local_dir, exist_ok=True)
        local_file_path = os.path.join(local_dir, file_name)
        with open(local_file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {file_url} to {local_file_path}")
    else:
        raise Exception(f"Failed to download file: {file_url}. Status code: {response.status_code}")

def main():
    base_url = "http://repos.net/2024/working/Nikel/"  # Replace with your target URL
    local_dir = "/path/to/local/destination"  # Replace with your local directory
    partial_file_name = "T-NKLDWWC_"  # Partial file name to search

    try:
        # Find the latest folder
        latest_folder_url = find_latest_folder(base_url)

        # Search for the specific file inside the latest folder
        file_url = find_specific_file(latest_folder_url, partial_file_name)

        if file_url:
            # Download the file
            download_file(file_url, local_dir)
        else:
            print(f"No file matching '{partial_file_name}' found in the latest folder.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()