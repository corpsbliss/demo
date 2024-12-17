import os
import requests
import zipfile
import shutil
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


def search_file_in_subdirectories(folder_url, partial_file_name, subdirectory):
    """
    Search for a specific file inside a specific subdirectory and its subdirectories.
    Recursively search all subdirectories.
    """
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
            if href.endswith('/'):
                print(f"Entering subdirectory: {full_url}")
                file_url = search_file_in_subdirectories(full_url, partial_file_name, "")
                if file_url:
                    return file_url

            if partial_file_name in href:
                print(f"Found file: {full_url}")
                return full_url

    return None


def download_file(file_url, destination_folder):
    """
    Download the specified file to the local directory with a progress bar.
    """
    response = requests.get(file_url, stream=True)

    if response.status_code != 200:
        raise Exception(f"Failed to download file: {file_url}. Status code: {response.status_code}")

    os.makedirs(destination_folder, exist_ok=True)
    file_name = os.path.basename(file_url)
    file_path = os.path.join(destination_folder, file_name)

    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    chunk_size = 8192

    print(f"Downloading {file_name} ({total_size / 1024 / 1024:.2f} MB)")

    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                file.write(chunk)
                downloaded += len(chunk)
                show_progress_bar(downloaded, total_size)

    print(f"\nFile downloaded: {file_path}")
    return file_path


def show_progress_bar(current, total, bar_length=50):
    """
    Display a progress bar for the download process.
    """
    progress = current / total
    block = int(bar_length * progress)
    bar = f"[{'#' * block}{'.' * (bar_length - block)}] {progress * 100:.2f}%"
    print(f"\r{bar}", end="")


def extract_and_replace(file_path, destination_folder):
    """
    Extract the downloaded ZIP file, replacing any existing folder.
    """
    if not zipfile.is_zipfile(file_path):
        raise Exception(f"The file is not a valid ZIP archive: {file_path}")

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        folder_name = zip_ref.namelist()[0].split('/')[0]
        extracted_folder_path = os.path.join(destination_folder, folder_name)

        if os.path.exists(extracted_folder_path):
            print(f"Deleting existing folder: {extracted_folder_path}")
            shutil.rmtree(extracted_folder_path)

        zip_ref.extractall(destination_folder)
        print(f"Extracted to: {extracted_folder_path}")

    os.remove(file_path)  # Remove the ZIP file after extraction
    return extracted_folder_path


def copy_to_destination(extracted_folder, copy_to_path):
    """
    Copy the extracted folder to the specified location, replacing if necessary.
    """
    destination = os.path.join(copy_to_path, os.path.basename(extracted_folder))

    if os.path.exists(destination):
        print(f"Deleting existing folder at destination: {destination}")
        shutil.rmtree(destination)

    shutil.copytree(extracted_folder, destination)
    print(f"Copied folder to: {destination}")


def main():
    base_url = "http://repos.net/2024/working/Nikel/"  # Replace with your target URL
    partial_file_name = "T-NKLDWWC_"  # Partial file name to search
    destination_folder = "/path/to/local/destination"  # Replace with your local folder
    copy_to_path = "/path/to/final/destination"  # Replace with the copy destination
    subdirectory = "images/T-NKLDWWC-REL/"  # Subdirectory to search in

    try:
        # Step 1: Identify the latest folder
        latest_folder_url = get_latest_folder(base_url)

        # Step 2: Search for the specific file in the specific subdirectory and its subdirectories
        file_url = search_file_in_subdirectories(latest_folder_url, partial_file_name, subdirectory)

        if file_url:
            # Step 3: Download the file
            downloaded_file = download_file(file_url, destination_folder)

            # Step 4: Extract the file and replace the folder if it exists
            extracted_folder = extract_and_replace(downloaded_file, destination_folder)

            # Step 5: Copy the extracted folder to the final destination
            copy_to_destination(extracted_folder, copy_to_path)
        else:
            print(f"No file found matching: {partial_file_name} inside {subdirectory} or its subdirectories")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()