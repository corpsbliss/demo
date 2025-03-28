import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_latest_folder(base_url):
    """
    Find the latest folder under the given base URL.
    """
    response = requests.get(base_url)
    if response.status_code != 200:
        raise Exception(f"Failed to access {base_url}. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    folders = []

    for link in soup.find_all('a'):
        href = link.get('href')
        # Only consider links ending with '/' (folders)
        if href and href.endswith('/'):
            folders.append(href)

    if not folders:
        raise Exception(f"No folders found at {base_url}")

    # Sort folder names alphabetically and pick the latest one
    latest_folder = sorted(folders)[-1]
    latest_folder_url = urljoin(base_url, latest_folder)
    print(f"Latest folder: {latest_folder_url}")
    return latest_folder_url

def search_file_in_specific_subdirectory(folder_url, partial_file_name, subdirectory):
    """
    Search for a specific file inside a specific subdirectory and its subdirectories.
    """
    # Construct the full path to the subdirectory
    subdirectory_url = urljoin(folder_url, subdirectory)
    
    response = requests.get(subdirectory_url)
    if response.status_code != 200:
        raise Exception(f"Failed to access {subdirectory_url}. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a'):
        href = link.get('href')
        if not href:
            continue

        full_url = urljoin(subdirectory_url, href)

        # Ensure we are only navigating inside the target subdirectory
        if full_url.startswith(subdirectory_url):  
            # Check if the file matches the search criteria
            if partial_file_name in href:
                print(f"Found file: {full_url}")
                return full_url

    return None

def download_file(file_url, destination_folder):
    """
    Download the specified file to the local directory.
    """
    response = requests.get(file_url, stream=True)

    if response.status_code != 200:
        raise Exception(f"Failed to download file: {file_url}. Status code: {response.status_code}")

    os.makedirs(destination_folder, exist_ok=True)
    file_name = os.path.basename(file_url)
    file_path = os.path.join(destination_folder, file_name)

    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f"File downloaded: {file_path}")

def main():
    base_url = "http://repos.net/2024/working/Nikel/"  # Replace with your target URL
    partial_file_name = "T-NKLDWWC_"  # Partial file name to search
    destination_folder = "/path/to/local/destination"  # Replace with your local folder
    subdirectory = "images/T-NKLDWWC-REL/"  # Subdirectory to search in

    try:
        # Step 1: Identify the latest folder
        latest_folder_url = get_latest_folder(base_url)

        # Step 2: Search for the specific file in the specific subdirectory
        file_url = search_file_in_specific_subdirectory(latest_folder_url, partial_file_name, subdirectory)

        if file_url:
            # Step 3: Download the file
            download_file(file_url, destination_folder)
        else:
            print(f"No file found matching: {partial_file_name} inside {subdirectory}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()